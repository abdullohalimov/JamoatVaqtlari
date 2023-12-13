# Generated by Django 5.0 on 2023-12-13 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text="Adminning Telegramdagi ID'si", max_length=255, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Admin ismi', max_length=255, verbose_name='Ismi')),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Adminlar',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(help_text='Tumanning lotincha nomi', max_length=255, verbose_name='Lotin')),
                ('name_cyrl', models.CharField(blank=True, help_text='Tumanning krillcha nomi', max_length=255, null=True, verbose_name='Krill')),
                ('name_ru', models.CharField(blank=True, help_text='Tumanning ruscha nomi', max_length=255, null=True, verbose_name='Rus')),
            ],
            options={
                'verbose_name': 'Tuman',
                'verbose_name_plural': 'Tumanlar',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(help_text='Viloyat/Shaxarning lotincha nomi', max_length=255, verbose_name='Lotin')),
                ('name_cyrl', models.CharField(blank=True, help_text='Viloyat/Shaxarning krillcha nomi', max_length=255, null=True, verbose_name='Krill')),
                ('name_ru', models.CharField(blank=True, help_text='Viloyat/Shaxarning ruscha nomi', max_length=255, null=True, verbose_name='Rus')),
            ],
            options={
                'verbose_name': 'Viloyat/Shaxar',
                'verbose_name_plural': 'Viloyat/Shaxarlar',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text="Foydalanuvchining Telegramdagi ID'si", max_length=255, verbose_name='ID')),
                ('full_name', models.TextField(blank=True, help_text='Foydalanuvchi ismi', null=True, verbose_name='Ismi')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='Masjid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(help_text='Masjidning lotincha nomi', max_length=255, verbose_name='Lotin')),
                ('name_cyrl', models.CharField(blank=True, help_text='Masjidning krillcha nomi', max_length=255, null=True, verbose_name='Krill')),
                ('name_ru', models.CharField(blank=True, help_text='Masjidning ruscha nomi', max_length=255, null=True, verbose_name='Rus')),
                ('photo', models.CharField(blank=True, help_text='Masjidning rasmi IDsi', max_length=255, null=True, verbose_name='Rasm IDsi')),
                ('photo_file', models.FileField(blank=True, help_text='Masjidning rasm faylini yuklang', max_length=255, null=True, upload_to='', verbose_name='Rasm fayli')),
                ('bomdod', models.CharField(help_text="Masjidda bomdod namozi o'qilish vaqti", max_length=255, verbose_name='Bomdod')),
                ('peshin', models.CharField(help_text="Masjidda peshin namozi o'qilish vaqti", max_length=255, verbose_name='Peshin')),
                ('asr', models.CharField(help_text="Masjidda asr namozi o'qilish vaqti", max_length=255, verbose_name='Asr')),
                ('shom', models.CharField(help_text="Masjidda shom namozi o'qilish vaqti", max_length=255, verbose_name='Shom')),
                ('hufton', models.CharField(help_text="Masjidda hufton namozi o'qilish vaqti", max_length=255, verbose_name='Hufton')),
                ('district', models.ForeignKey(help_text='Masjid joylashgan tuman', on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.district', verbose_name='Tuman')),
            ],
            options={
                'verbose_name': 'Masjid',
                'verbose_name_plural': 'Masjidlar',
            },
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(help_text='Tuman joylashgan viloyat/shaxar', on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.region', verbose_name='Viloyat/Shaxar'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masjid', models.ForeignKey(blank=True, help_text='Masjid', null=True, on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.masjid', verbose_name='Masjid')),
                ('user', models.ForeignKey(help_text='Foydalanuvchi', on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.user', verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Obuna',
                'verbose_name_plural': 'Obunalar',
            },
        ),
    ]
