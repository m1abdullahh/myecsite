# Generated by Django 4.2.3 on 2023-07-12 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0003_product_additional_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_id',
            field=models.CharField(default='', max_length=200),
        ),
    ]
