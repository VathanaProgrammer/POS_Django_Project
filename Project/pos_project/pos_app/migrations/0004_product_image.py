# Generated by Django 5.1.4 on 2025-03-23 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0003_alter_category_name_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
