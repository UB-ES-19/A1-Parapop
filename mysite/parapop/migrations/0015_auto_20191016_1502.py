# Generated by Django 2.2.5 on 2019-10-16 13:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parapop', '0014_auto_20191015_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpost',
            name='favUsers',
            field=models.ManyToManyField(blank=True, related_name='favUsers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productpost',
            name='productPic',
            field=models.FileField(upload_to='product_pics/'),
        ),
    ]
