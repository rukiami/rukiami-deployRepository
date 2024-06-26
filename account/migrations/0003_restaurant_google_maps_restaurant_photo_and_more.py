# Generated by Django 4.1 on 2024-02-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_restaurant_address_restaurant_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='google_maps',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='restaurant_photos/'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='price_range',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
