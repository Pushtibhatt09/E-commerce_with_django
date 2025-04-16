from django.urls import path
from .views import HomeView, ProductDetailView, ContactPageView, FAQPageView, TermsPageView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('faq/', FAQPageView.as_view(), name='faq'),
    path('terms/', TermsPageView.as_view(), name='terms')
]