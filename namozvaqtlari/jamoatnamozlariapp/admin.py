from django.contrib import admin
from .models import User, Region, Admin, District, Masjid, Subscription

# Register your models here.

class MasjidAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru', 'photo_file', 'district']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru', 'region']

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_cyrl', 'name_ru']

class SubscriptionAdmin(admin.ModelAdmin):  
    list_display = ['user', 'masjid']

class AdminModelAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_id']

class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_id', ]





admin.site.register(User, UserAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Admin, AdminModelAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Masjid, MasjidAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
