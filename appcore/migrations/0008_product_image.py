# Generated by Django 4.2.3 on 2023-07-17 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0007_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
            preserve_default=False,
        ),
    ]