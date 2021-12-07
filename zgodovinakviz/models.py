from django.conf import settings
from django.db import models
from django.utils import timezone


class Vprasanje(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vprasanje = models.CharField(max_length=1000)
    pravilen_odgovor = models.CharField(max_length=1000)
    napacen_odgovor_1 = models.CharField(max_length=1000)
    napacen_odgovor_2 = models.CharField(max_length=1000)
    namig = models.CharField(max_length=1000)
    slika = models.CharField(max_length=1000)
    level = models.CharField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vprasanje

class Odgovor(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vprasanje = models.ForeignKey(Vprasanje, on_delete=models.CASCADE)
    pravilen = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vprasanje