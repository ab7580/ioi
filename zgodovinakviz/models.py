from django.conf import settings
from django.db import models
from django.utils import timezone

class Level(models.Model):
    ime = models.CharField(max_length=1000)
    vrstni_red = models.IntegerField()

    def __str__(self):
        return self.ime


class Uporabnik(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    ucitelj = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Slika(models.Model):
    slika = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.slika.name

class Vprasanje(models.Model):
    author = models.ForeignKey(Uporabnik, on_delete=models.SET_NULL, null=True)
    vprasanje = models.CharField(max_length=1000)
    pravilen_odgovor = models.CharField(max_length=1000)
    napacen_odgovor_1 = models.CharField(max_length=1000)
    napacen_odgovor_2 = models.CharField(max_length=1000)
    namig = models.CharField(max_length=1000)
    slika = models.ForeignKey(Slika, on_delete=models.SET_NULL, null=True)
    slika_name = models.CharField(max_length=1000, default="")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    locked = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vprasanje


class Odgovor(models.Model):
    author = models.ForeignKey(Uporabnik, on_delete=models.SET_NULL, null=True)
    vprasanje = models.ForeignKey(Vprasanje, on_delete=models.SET_NULL, null=True)
    izbran_odgovor = models.CharField(max_length=1000)
    pravilen = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.author.user.username + ": " + (self.vprasanje.vprasanje if self.vprasanje else "Izbrisano vpra??anje")


class PrikazanaVprasanja(models.Model):
    vprasanje = models.ForeignKey(Vprasanje, on_delete=models.CASCADE)
    uporabnik = models.ForeignKey(Uporabnik, on_delete=models.CASCADE)

    def __str__(self):
        return "Uporabniku " + self.uporabnik.user.first_name + " se prikazuje vprasanje " + self.vprasanje.vprasanje + " DO NOT ADD MANUALLY"