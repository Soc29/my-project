# Generated by Django 3.1.7 on 2021-02-23 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='イメージ画像'),
        ),
    ]
