from django.contrib import admin
from .models import Vprasanje
from .models import Odgovor

admin.site.register(Vprasanje)
admin.site.register(Odgovor)