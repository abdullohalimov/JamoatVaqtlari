# Generated by Django 5.0 on 2023-12-20 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0002_customuser_admin_type_customuser_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='admin_type',
            field=models.CharField(choices=[('region', 'Region Admin'), ('district', 'District Admin'), ('masjid', 'Masjid Admin')], help_text='Admin type', max_length=255, null=True, verbose_name='Admin type'),
        ),
    ]
