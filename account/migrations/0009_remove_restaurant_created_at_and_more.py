# Generated by Django 4.1 on 2024-03-02 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_restaurant_created_at_restaurant_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='updated_at',
        ),
    ]
