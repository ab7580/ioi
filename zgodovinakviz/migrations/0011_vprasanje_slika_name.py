# Generated by Django 3.2.9 on 2022-01-02 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zgodovinakviz', '0010_uporabnik_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='vprasanje',
            name='slika_name',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
