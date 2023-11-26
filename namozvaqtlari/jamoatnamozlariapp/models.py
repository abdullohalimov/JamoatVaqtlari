from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=255)
    full_name = models.TextField(null=True)

class Admin(models.Model):
    user_id = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    
class Region(models.Model):
    name_uz = models.CharField(max_length=255)
    name_cyrl = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class District(models.Model):
    name_uz = models.CharField(max_length=255)
    name_cyrl = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class Mosque(models.Model):
    name_uz = models.CharField(max_length=255)
    name_cyrl = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE)