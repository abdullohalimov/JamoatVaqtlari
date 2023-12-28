# jamoatnamozlariapp/urls.py
from django.urls import path
from .views import your_custom_view

urlpatterns = [
    path('custom-view/', your_custom_view, name='your_custom_view'),
]
