# Generated by Django 3.2.9 on 2021-12-09 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zgodovinakviz', '0003_auto_20211208_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vprasanje',
            name='level',
        ),
    ]
