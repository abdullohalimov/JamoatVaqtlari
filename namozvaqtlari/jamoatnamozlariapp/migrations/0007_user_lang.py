# Generated by Django 5.0 on 2023-12-21 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0006_alter_customuser_admin_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lang',
            field=models.CharField(blank=True, help_text='Til', max_length=255, null=True, verbose_name='Til'),
        ),
    ]
