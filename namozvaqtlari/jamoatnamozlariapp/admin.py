import logging
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as usrmadmin
from django import forms
from .models import (
    Mintaqa,
    NamozVaqti,
    User,
    Region,
    Admin,
    District,
    Masjid,
    Subscription,
    CustomUser
)

# Register your models here.

class MasjidForm(forms.ModelForm):
    class Meta:
        model = Masjid
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        logging.warning(user)
        logging.warning(kwargs)
        super(MasjidForm, self).__init__(*args, **kwargs)
        # logging.warning(self)
        # logging.warning(args)
        # logging.warning(kwargs)
        # try:
        #     instance = kwargs.get("instance", None)
        #     self.fields["tuman"].queryset = District.objects.filter(
        #         self.
        #     )
        #     self.fields["schedule"].queryset = District.objects.filter(
        #         guruh=instance.group
        #     )
        # except:
        #     pass

class CustomUserAdmin(usrmadmin):
    model = CustomUser
    fieldsets = (
                    
        (None, {"fields": ("username", "password", "region",)}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "region"),
            },
        ),
    )
class MasjidAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "photo_file", "district"]
    form = MasjidForm
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(district__region__pk=request.user.region.pk)



class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "region"]


class RegionAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru"]
    search_fields = ["name_uz", "name_cyrl", "name_ru"]


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
admin.site.register(CustomUser, CustomUserAdmin)