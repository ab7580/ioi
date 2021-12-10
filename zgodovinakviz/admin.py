from django.contrib import admin
from .models import Vprasanje
from .models import Odgovor
from .models import Level
from .models import Uporabnik
from .models import PrikazanaVprasanja

admin.site.register(Vprasanje)
admin.site.register(Odgovor)
admin.site.register(Level)
admin.site.register(Uporabnik)
admin.site.register(PrikazanaVprasanja)