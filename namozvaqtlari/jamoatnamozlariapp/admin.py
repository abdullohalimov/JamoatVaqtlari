from django.contrib import admin
from .models import User, Region, Admin, District, Mosque, Subscription

# Register your models here.

class MosqueAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru', 'photo', 'district']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru', 'region']

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru']

class SubscriptionAdmin(admin.ModelAdmin):  
    list_display = ['name_uz', 'name_cyrl', 'name_ru']

class AdminAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru']

class UserAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru']





admin.site.register(User)
admin.site.register(Region)
admin.site.register(Admin)
admin.site.register(District)
admin.site.register(Mosque)
admin.site.register(Subscription)
