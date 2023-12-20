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
    CustomUser,
)

# Register your models here.


class CustomUserAdmin(usrmadmin):
    model = CustomUser
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "region",
                    "district",
                    "masjid",
                    "admin_type",
                )
            },
        ),
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
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "region",
                    "district",
                    "masjid",
                    "admin_type",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )


class MasjidAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "photo_file", "district"]
    # form = MasjidForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "district":
            # Filter choices based on the assigned region for custom admins
            if not request.user.is_superuser and request.user.admin_type == "region":
                kwargs["queryset"] = District.objects.filter(region=request.user.region)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(MasjidAdmin, self).get_form(request, obj=obj, **kwargs)
        form.base_fields["district"].initial = request.user.district

        if request.user.is_superuser or request.user.admin_type == "region":
            # If superadmin, make the 'district' field editable
            form.base_fields["district"].widget.attrs["disabled"] = False
        else:
            # If not superadmin, make the 'district' field readonly
            form.base_fields["district"].widget.attrs["disabled"] = True
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.admin_type == "region":
            return qs.filter(district__region__pk=request.user.region.pk)
        elif request.user.admin_type == "district":
            return qs.filter(district__pk=request.user.district.pk)
        elif request.user.admin_type == "masjid":
            return qs.filter(pk=request.user.masjid.pk)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "region"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "district":
            # Filter choices based on the assigned region for custom admins
            if not request.user.is_superuser and request.user.admin_type == "region":
                kwargs["queryset"] = Region.objects.filter(region=request.user.region)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DistrictAdmin, self).get_form(request, obj=obj, **kwargs)
        form.base_fields["region"].initial = request.user.region

        if request.user.is_superuser:
            # If superadmin, make the 'district' field editable
            form.base_fields["region"].widget.attrs["disabled"] = False
        else:
            # If not superadmin, make the 'district' field readonly
            form.base_fields["region"].widget.attrs["disabled"] = True
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.admin_type == "region":
            return qs.filter(region__pk=request.user.region.pk)
        elif request.user.admin_type == "district":
            return qs.filter(region__pk=request.user.district.region.pk)


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
    list_display = [
        "mintaqa",
        "milodiy_oy",
        "milodiy_kun",
        "xijriy_oy",
        "xijriy_kun",
        "vaqtlari",
    ]
    autocomplete_fields = ["mintaqa"]


admin.site.register(User, UserAdmin)
admin.site.register(Region, RegionAdmin)
# admin.site.register(Admin, AdminModelAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Masjid, MasjidAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Mintaqa, MintaqaAdmin)
admin.site.register(NamozVaqti, NamozVaqtiAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
