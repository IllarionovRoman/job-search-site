# Generated by Django 3.2.8 on 2021-10-09 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='job',
        ),
    ]
