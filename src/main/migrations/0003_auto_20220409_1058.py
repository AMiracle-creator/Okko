# Generated by Django 3.2.8 on 2022-04-09 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_metricsmodel_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricsmodel',
            name='material',
        ),
        migrations.AddField(
            model_name='metricsmodel',
            name='link',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]