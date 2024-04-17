# Generated by Django 4.1 on 2024-04-15 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_alter_photo_image'),
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
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='restaurant_photos/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='photo',
            field=models.ImageField(upload_to='restaurant_photos/'),
        ),
    ]