# Generated by Django 2.1 on 2020-05-25 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapps', '0009_remove_statusdetail_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='osanddevicedetail',
            name='is_active',
        ),
    ]
