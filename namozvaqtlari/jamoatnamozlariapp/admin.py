from django.contrib import admin
from .models import (
    Mintaqa,
    NamozVaqti,
    User,
    Region,
    Admin,
    District,
    Masjid,
    Subscription,
)

# Register your models here.


class MasjidAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "photo_file", "district"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "region"]


class RegionAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru"]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "masjid"]


class AdminModelAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user_id"]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "user_id",
    ]


class MintaqaAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "viloyat", "mintaqa_id"]
    search_fields = ["name_uz", "name_cyrl", "name_ru", "viloyat"]


class NamozVaqtiAdmin(admin.ModelAdmin):
    list_display = ["mintaqa", "milodiy_oy", "milodiy_kun", "xijriy_oy", "xijriy_kun",  "vaqtlari"]
    autocomplete_fields = ["mintaqa"]


admin.site.register(User, UserAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Admin, AdminModelAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Masjid, MasjidAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Mintaqa, MintaqaAdmin)
admin.site.register(NamozVaqti, NamozVaqtiAdmin)
