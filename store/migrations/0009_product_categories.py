# Generated by Django 4.2.11 on 2024-08-04 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='store.category'),
        ),
    ]