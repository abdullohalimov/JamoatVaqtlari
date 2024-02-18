# Generated by Django 5.0.2 on 2024-02-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0019_remove_shaxarviloyattimeschange_asr_jamoat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masjid',
            name='asr_jamoat',
            field=models.CharField(default='0', help_text='Masjidda asr namozi oʻqilish vaqti', max_length=255, verbose_name='Asr jamoati'),
        ),
        migrations.AlterField(
            model_name='masjid',
            name='bomdod_jamoat',
            field=models.CharField(default='0', help_text='Masjidda bomdod namozi oʻqilish vaqti', max_length=255, verbose_name='Bomdod jamoati'),
        ),
        migrations.AlterField(
            model_name='masjid',
            name='hufton_jamoat',
            field=models.CharField(default='0', help_text='Masjidda xufton namozi oʻqilish vaqti', max_length=255, verbose_name='Xufton jamoati'),
        ),
        migrations.AlterField(
            model_name='masjid',
            name='peshin_jamoat',
            field=models.CharField(default='0', help_text='Masjidda peshin namozi oʻqilish vaqti', max_length=255, verbose_name='Peshin jamoati'),
        ),
        migrations.AlterField(
            model_name='masjid',
            name='shom_jamoat',
            field=models.CharField(default='0', help_text='Masjidda shom namozi oʻqilish vaqti', max_length=255, verbose_name='Shom jamoati'),
        ),
    ]
