# Generated by Django 3.2.9 on 2022-01-02 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zgodovinakviz', '0008_uporabnik_ucitelj'),
    ]

    operations = [
        migrations.AddField(
            model_name='vprasanje',
            name='locked',
            field=models.BooleanField(default=False),
        ),
    ]
