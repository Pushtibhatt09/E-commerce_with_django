from django.urls import path
from .views import HomeView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]