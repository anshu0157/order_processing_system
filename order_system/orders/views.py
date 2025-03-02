from .models import Order
import queue, threading, time
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import OrderSerializer
from django.db.models import Count, Avg, F

# In-memory queue
order_queue = queue.Queue()

# Worker Function
def process_orders():
    while True:
        order_id = order_queue.get()
        if order_id is None:
            break
        
        order = Order.objects.get(order_id=order_id)
        time.sleep(2)
        order.status = 'Processing'
        order.save()
        time.sleep(3)  # order processing completed after 3 seconds
        order.status = 'Completed'
        order.save()
        order_queue.task_done()

# Start worker thread
worker_thread = threading.Thread(target=process_orders, daemon=True)
worker_thread.start()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """Create Order & Add to Queue"""
        data = request.data.copy()
        # Remove CSRF token if present
        data.pop("csrfmiddlewaretoken", None)

        # Serialize and validate data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()  # Save order to DB
            order_queue.put(order.order_id)  # Add order to queue
            return Response({"message": "Order received.", "order_id": f"ORD{order.order_id}"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Check Order Status"""
        order = self.get_object()
        return Response({'order_id': f"ORD{order.order_id}", 'status': order.status})

    @action(detail=False, methods=['get'])
    def metrics(self, request):
        """Fetch Metrics"""
        total_orders = Order.objects.count()
        # Get order counts by status
        status_counts = Order.objects.values('status').annotate(count=Count('status'))
        order_status_counts = {entry['status']: entry['count'] for entry in status_counts}
        
        # Get average processing time (only for completed orders)
        avg_processing_time = Order.objects.filter(status="completed",createdOn__isnull=False).annotate(
            processing_time=F('updatedOn') - F('createdOn')).aggregate(Avg('processing_time'))['processing_time__avg']

        # Convert processing time to seconds
        avg_processing_time_seconds = avg_processing_time.total_seconds() if avg_processing_time else 0

        # Prepare response
        metrics_data = {
            "total_orders_processed": total_orders,
            "average_processing_time_seconds": avg_processing_time_seconds,
            "order_status_counts": order_status_counts
        }

        return Response(metrics_data)
