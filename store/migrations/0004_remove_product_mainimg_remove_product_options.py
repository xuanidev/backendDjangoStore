# Generated by Django 4.2.14 on 2024-07-31 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_personalization_image_product_main_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='mainImg',
        ),
        migrations.RemoveField(
            model_name='product',
            name='options',
        ),
    ]