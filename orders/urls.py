from django.urls import path
from .views import OrderListView, OrderDetailView, CancelOrderView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('view/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('cancel/<int:pk>/', CancelOrderView.as_view(), name='cancel_order'),
]



