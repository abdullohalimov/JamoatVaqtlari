# jamoatnamozlariapp/urls.py
from django.urls import path
from .views import your_custom_view, masjid_statistics, region_statistics, district_statistics

urlpatterns = [
    path('masjid_s/', masjid_statistics, name='masjid_statistic'),
    path('region_s/', region_statistics, name='region_statistic'),
    path('district_s/', district_statistics, name='district_statistic'),
    path('custom-view/', your_custom_view, name='your_custom_view'),
]
