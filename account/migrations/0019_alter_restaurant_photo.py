# Generated by Django 4.1 on 2024-04-17 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='restaurant_photos/'),
        ),
    ]