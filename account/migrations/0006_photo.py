# Generated by Django 4.1 on 2024-02-21 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_restaurant_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='restaurant_photos/')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='account.restaurant')),
            ],
        ),
    ]
