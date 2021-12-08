from django.contrib import admin
from .models import Vprasanje
from .models import Odgovor
from .models import Level

admin.site.register(Vprasanje)
admin.site.register(Odgovor)
admin.site.register(Level)