# Generated by Django 5.0.6 on 2024-07-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployersApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobadvertisement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ به روز رسانی'),
        ),
    ]
