# Generated by Django 2.2.5 on 2019-10-14 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parapop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpost',
            name='date_posted',
        ),
    ]
