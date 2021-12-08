from django.conf import settings
from django.db import models
from django.utils import timezone

class Level(models.Model):
    ime = models.CharField(max_length=1000)
    vrstni_red = models.IntegerField()

class Vprasanje(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    vprasanje = models.CharField(max_length=1000)
    pravilen_odgovor = models.CharField(max_length=1000)
    napacen_odgovor_1 = models.CharField(max_length=1000)
    napacen_odgovor_2 = models.CharField(max_length=1000)
    namig = models.CharField(max_length=1000)
    slika = models.CharField(max_length=1000)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vprasanje

class Odgovor(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    vprasanje = models.ForeignKey(Vprasanje, on_delete=models.SET_NULL, null=True)
    pravilen = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vprasanje