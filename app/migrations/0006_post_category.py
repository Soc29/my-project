# Generated by Django 3.1.7 on 2021-03-05 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='カテゴリ'),
            preserve_default=False,
        ),
    ]
