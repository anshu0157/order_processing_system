from django.db import models

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    ]

    user_id = models.IntegerField()
    order_id = models.AutoField(primary_key=True)
    item_ids = models.JSONField()  # List of item ids
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return f" orderId: ORD{self.order_id} - {self.status}"