# Generated by Django 2.1 on 2020-05-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapps', '0005_auto_20200521_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testscriptdetail',
            name='test_script',
        ),
        migrations.AddField(
            model_name='testscriptdetail',
            name='title',
            field=models.CharField(default=2020, max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TestScript',
        ),
    ]
