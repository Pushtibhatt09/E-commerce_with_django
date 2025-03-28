from django.db import models
from stylique_core.models.users import User
from stylique_core.models.store import Product
from datetime import datetime


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def generate_invoice_number(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"INV-{timestamp}-{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
