# Generated by Django 4.2.3 on 2023-07-17 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0004_product_price_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_path',
            field=models.ImageField(upload_to='', verbose_name='Image Path'),
        ),
    ]
