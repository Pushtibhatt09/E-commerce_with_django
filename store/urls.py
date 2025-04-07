from django.urls import path
from store.views import home

urlpatterns = [
    path('', home, name='home'),
]
