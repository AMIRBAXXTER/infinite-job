# Generated by Django 5.0.6 on 2024-07-17 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployersApp', '0002_jobadvertisement_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobadvertisement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد'),
        ),
    ]
