# Generated by Django 5.0.1 on 2024-01-23 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamoatnamozlariapp', '0015_changedistricttimeschedule_changemasjidtimeschedule_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='changedistricttimeschedule',
            options={'verbose_name': 'Tuman(Shahar) vaqtlarini oʻzgartirish jadvali', 'verbose_name_plural': 'Tuman(Shahar) vaqtlarini oʻzgartirish jadvali'},
        ),
        migrations.AlterModelOptions(
            name='changemasjidtimeschedule',
            options={'verbose_name': 'Masjid vaqtlarini oʻzgartirish jadvali', 'verbose_name_plural': 'Masjid vaqtlarini oʻzgartirish jadvali'},
        ),
        migrations.AlterModelOptions(
            name='changeregiontimeschedule',
            options={'verbose_name': 'Viloyat vaqtlarini oʻzgartirish jadvali', 'verbose_name_plural': 'Viloyat vaqtlarini oʻzgartirish jadvali'},
        ),
        migrations.AlterField(
            model_name='changedistricttimeschedule',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.district', verbose_name='Tuman(Shahar)'),
        ),
        migrations.AlterField(
            model_name='changemasjidtimeschedule',
            name='masjid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.masjid', verbose_name='Masjid'),
        ),
        migrations.AlterField(
            model_name='changeregiontimeschedule',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jamoatnamozlariapp.region', verbose_name='Viloyat'),
        ),
    ]