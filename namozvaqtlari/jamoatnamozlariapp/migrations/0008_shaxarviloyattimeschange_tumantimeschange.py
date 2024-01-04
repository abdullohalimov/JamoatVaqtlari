# Generated by Django 5.0 on 2023-12-25 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0007_user_lang'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShaxarViloyatTimesChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bomdod', models.CharField(help_text='Bomdod vaqti', max_length=255, verbose_name='Bomdod')),
                ('peshin', models.CharField(help_text='Peshin vaqti', max_length=255, verbose_name='Peshin')),
                ('asr', models.CharField(help_text='Asr vaqti', max_length=255, verbose_name='Asr')),
                ('shom', models.CharField(help_text='Shom vaqti', max_length=255, verbose_name='Shom')),
                ('xufton', models.CharField(help_text='Xufton vaqti', max_length=255, verbose_name='Xufton')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.region', verbose_name='Shaxar/Viloyat')),
            ],
            options={
                'verbose_name': "Shaxar/Viloyat namoz vaqtlarini o'zgartirish",
                'verbose_name_plural': "Shaxar/Viloyat vaqtlarini o'zgartirish",
            },
        ),
        migrations.CreateModel(
            name='TumanTimesChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bomdod', models.CharField(help_text='Bomdod vaqti', max_length=255, verbose_name='Bomdod')),
                ('peshin', models.CharField(help_text='Peshin vaqti', max_length=255, verbose_name='Peshin')),
                ('asr', models.CharField(help_text='Asr vaqti', max_length=255, verbose_name='Asr')),
                ('shom', models.CharField(help_text='Shom vaqti', max_length=255, verbose_name='Shom')),
                ('xufton', models.CharField(help_text='Xufton vaqti', max_length=255, verbose_name='Xufton')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.district', verbose_name='Tuman')),
            ],
            options={
                'verbose_name': "Tuman namoz vaqtlarini o'zgartirish",
                'verbose_name_plural': "Tuman namoz vaqtlarini o'zgartirish",
            },
        ),
    ]
