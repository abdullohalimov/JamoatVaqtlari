from django.contrib import admin
from .models import User, Region, Admin, District, Mosque, Subscription

# Register your models here.


admin.site.register(User)
admin.site.register(Region)
admin.site.register(Admin)
admin.site.register(District)
admin.site.register(Mosque)
admin.site.register(Subscription)
