# Generated by Django 2.2.5 on 2019-10-14 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parapop', '0002_remove_productpost_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpost',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
