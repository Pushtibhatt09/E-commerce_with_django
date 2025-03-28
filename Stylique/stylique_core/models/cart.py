from django.db import models
from stylique_core.models.users import User
from stylique_core.models.store import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.items = None

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def update_total(self):
        self.total_price = sum(item.subtotal_price for item in self.items.all())
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.cart.user.username} - {self.quantity} x {self.product.name}"




