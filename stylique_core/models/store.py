from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from stylique_core.models.users import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.reviews = None

    def __str__(self):
        return self.name

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews:
            self.rating = sum(review.rating for review in reviews) / reviews.count()
        else:
            self.rating = 0
        self.save()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s review on {self.product.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()
