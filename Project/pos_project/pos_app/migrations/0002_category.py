# Generated by Django 5.1.4 on 2025-03-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
