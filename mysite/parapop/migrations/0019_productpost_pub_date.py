# Generated by Django 2.2.7 on 2019-12-18 20:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parapop', '0018_delete_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpost',
            name='pub_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]