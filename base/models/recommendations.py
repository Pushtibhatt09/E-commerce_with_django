from django.db import models
from django.contrib.auth import get_user_model
from base.models.store import Product

User = get_user_model()


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendations for {self.user.username}"


class RecommendedProduct(models.Model):
    recommendation = models.ForeignKey(
        Recommendation, on_delete=models.CASCADE, related_name='products'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.FloatField(default=0, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recommendation', 'product'], name='unique_recommendation_product')
        ]
        ordering = ['-score']

    def __str__(self):
        return f"{self.product.name} (Score: {self.score}) recommended for {self.recommendation.user.username if self.recommendation else 'Unknown'}"


class ProductView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{user_info} viewed {self.product.name} at {self.viewed_at}"
