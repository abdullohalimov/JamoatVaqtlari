from collections.abc import Iterable
from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=255, verbose_name="ID", help_text="Foydalanuvchining Telegramdagi ID'si")
    full_name = models.TextField(null=True, blank=True, verbose_name="Ismi", help_text="Foydalanuvchi ismi")

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

class Admin(models.Model):
    user_id = models.CharField(max_length=255, verbose_name="ID", help_text="Adminning Telegramdagi ID'si")
    full_name = models.CharField(max_length=255, verbose_name="Ismi", help_text="Admin ismi")

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Adminlar"

    
class Region(models.Model):
    name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Viloyat/Shaxarning lotincha nomi")
    name_cyrl = models.CharField(max_length=255, verbose_name="Krill", help_text="Viloyat/Shaxarning krillcha nomi", null=True, blank=True)
    name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Viloyat/Shaxarning ruscha nomi", null=True, blank=True)

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if self.name_cyrl == None:
            self.name_cyrl = self.name_uz
        if self.name_ru == None:
            self.name_ru = self.name_uz
        return super().save()

    def __str__(self):
        return self.name_uz
    
    class Meta:
        verbose_name = "Viloyat/Shaxar"
        verbose_name_plural = "Viloyat/Shaxarlar"


class District(models.Model):
    name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Tumanning lotincha nomi")
    name_cyrl = models.CharField(max_length=255, verbose_name="Krill", help_text="Tumanning krillcha nomi", null=True, blank=True)
    name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Tumanning ruscha nomi", null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Viloyat/Shaxar", help_text="Tuman joylashgan viloyat/shaxar")

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if self.name_cyrl == None:
            self.name_cyrl = self.name_uz
        if self.name_ru == None:
            self.name_ru = self.name_uz
        return super().save()

    def __str__(self):
        return self.name_uz
    
    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"


class Mosque(models.Model):
    name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Masjidning lotincha nomi")
    name_cyrl = models.CharField(max_length=255, verbose_name="Krill", help_text="Masjidning krillcha nomi", null=True, blank=True)
    name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Masjidning ruscha nomi", null=True, blank=True)
    photo = models.CharField(max_length=255, verbose_name="Rasmi", help_text="Masjidning rasmi")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Tuman", help_text="Masjid joylashgan tuman")
    bomdod = models.CharField(max_length=255, verbose_name="Bomdod", help_text="Masjidda bomdod namozi o'qilish vaqti")
    peshin = models.CharField(max_length=255, verbose_name="Peshin", help_text="Masjidda peshin namozi o'qilish vaqti")
    asr = models.CharField(max_length=255, verbose_name="Asr", help_text="Masjidda asr namozi o'qilish vaqti")
    shom = models.CharField(max_length=255, verbose_name="Shom", help_text="Masjidda shom namozi o'qilish vaqti")
    hufton = models.CharField(max_length=255, verbose_name="Hufton", help_text="Masjidda hufton namozi o'qilish vaqti")

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if self.name_cyrl == None:
            self.name_cyrl = self.name_uz
        if self.name_ru == None:
            self.name_ru = self.name_uz
        
        return super().save()

    def __str__(self):
        return self.name_uz
    
    class Meta:
        verbose_name = "Masjid"
        verbose_name_plural = "Masjidlar"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi", help_text="Foydalanuvchi")
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, verbose_name="Masjid", help_text="Masjid")

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        verbose_name = "Obuna"
        verbose_name_plural = "Obunalar"
        