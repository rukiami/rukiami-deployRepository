# Generated by Django 4.1 on 2024-02-19 08:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='address',
            field=models.TextField(default='your_default_value'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='date_added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='genre',
            field=models.CharField(default='Not specified', max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='location',
            field=models.TextField(),
        ),
    ]
