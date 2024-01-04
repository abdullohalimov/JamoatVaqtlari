# Generated by Django 5.0 on 2023-12-20 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='admin_type',
            field=models.CharField(help_text='Admin type', max_length=255, null=True, verbose_name='Admin type'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.district'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='masjid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.masjid'),
        ),
    ]
