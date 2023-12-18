from collections.abc import Iterable
from django.db import models

from .tg_functions import get_photo_id

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
    name_cyrl = models.CharField(max_length=255, verbose_name="Kirill", help_text="Viloyat/Shaxarning kirillcha nomi", null=True, blank=True)
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
    name_cyrl = models.CharField(max_length=255, verbose_name="Kirill", help_text="Tumanning kirillcha nomi", null=True, blank=True)
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


class Masjid(models.Model):
    name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Masjidning lotincha nomi")
    name_cyrl = models.CharField(max_length=255, verbose_name="Kirill", help_text="Masjidning kirillcha nomi", null=True, blank=True)
    name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Masjidning ruscha nomi", null=True, blank=True)
    photo = models.CharField(max_length=255, verbose_name="Rasm IDsi", help_text="Masjidning rasmi IDsi", null=True, blank=True)
    photo_file = models.FileField(max_length=255, verbose_name="Rasm fayli", help_text="Masjidning rasm faylini yuklang", null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Tuman", help_text="Masjid joylashgan tuman")
    bomdod = models.CharField(max_length=255, verbose_name="Bomdod", help_text="Masjidda bomdod namozi o'qilish vaqti")
    peshin = models.CharField(max_length=255, verbose_name="Peshin", help_text="Masjidda peshin namozi o'qilish vaqti")
    asr = models.CharField(max_length=255, verbose_name="Asr", help_text="Masjidda asr namozi o'qilish vaqti")
    shom = models.CharField(max_length=255, verbose_name="Shom", help_text="Masjidda shom namozi o'qilish vaqti")
    hufton = models.CharField(max_length=255, verbose_name="Xufton", help_text="Masjidda xufton namozi o'qilish vaqti")
    location = models.CharField(max_length=255, verbose_name="Manzil", help_text="Masjid manzili", null=True, blank=True)
    qisqa_tavsif = models.TextField(verbose_name="Qisqa tavsif", help_text="Masjid haqida qisqa tavsif", null=True, blank=True)
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if self.name_cyrl == None:
            self.name_cyrl = self.name_uz
        if self.name_ru == None:
            self.name_ru = self.name_uz

        if self.photo_file:
            if not self.photo:
                self.photo = get_photo_id(self.photo_file.file)
            else:
                old = Masjid.objects.get(pk=self.pk) 
                if self.photo != old.photo:
                    self.photo = get_photo_id(self.photo_file.file) 
        return super().save()

    def __str__(self):
        return self.name_uz
    
    class Meta:
        verbose_name = "Masjid"
        verbose_name_plural = "Masjidlar"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi", help_text="Foydalanuvchi")
    masjid = models.ForeignKey(Masjid, on_delete=models.CASCADE, verbose_name="Masjid", help_text="Masjid", null=True, blank=True)

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        verbose_name = "Obuna"
        verbose_name_plural = "Obunalar"
        
class Mintaqa(models.Model):
    viloyatlar = [
        ("1", "Toshkent"),
        ("2", "Andijon"),
        ("99", "Boshqa"),
    ]
    name_uz = models.CharField(max_length=255, verbose_name="Lotin", help_text="Mintaqaning lotincha nomi")
    name_cyrl = models.CharField(max_length=255, verbose_name="Kirill", help_text="Mintaqaning kirillcha nomi", null=True, blank=True)
    name_ru = models.CharField(max_length=255, verbose_name="Rus", help_text="Mintaqaning ruscha nomi", null=True, blank=True)
    mintaqa_id = models.CharField(max_length=255, verbose_name="Mintaqa IDsi", help_text="Mintaqaning IDsi")
    viloyat = models.CharField(max_length=255, choices=viloyatlar, verbose_name="Viloyat", help_text="Mintaqa joylashgan viloyat")

    class Meta:
        verbose_name = "Mintaqa"
        verbose_name_plural = "Mintaqalar"

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if self.name_cyrl == None:
            self.name_cyrl = self.name_uz
        if self.name_ru == None:
            self.name_ru = self.name_uz

        return super().save()
    

class NamozVaqti(models.Model):
    mintaqa = models.ForeignKey(Mintaqa, on_delete=models.CASCADE, verbose_name="Mintaqa", help_text="Mintaqa")
    milodiy_oy = models.IntegerField(max_length=255, verbose_name="Milodiy oy", help_text="Milodiy oy")
    xijriy_oy = models.IntegerField(max_length=255, verbose_name="Xijriy oy", help_text="Xijriy oy")
    milodiy_kun = models.IntegerField(max_length=255, verbose_name="Milodiy kun", help_text="Milodiy kun")
    xijriy_kun = models.IntegerField(max_length=255, verbose_name="Xijriy kun", help_text="Xijriy kun")
    vaqtlari = models.CharField(max_length=255, verbose_name="Vaqtlari", help_text="Tong | Quyosh | Peshin | Asr | Shom | Xufton")

    def __str__(self):
        return self.vaqti