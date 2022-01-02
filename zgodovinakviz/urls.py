from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.start, name='start'),
    path('vstop', views.vstopi, name='vstopi'),
    path('kviz', views.kviz, name='kviz'),
    path('vprasanje/dodaj', views.dodaj, name='dodaj'),
    path('vprasanje/<int:pk>/uredi', views.uredi, name='uredi'),
    path('vprasanje/<int:pk>', views.vprasanje, name='vprasanje'),
    path('vprasanje/<int:pk>/odstrani', views.odstrani, name='odstrani'),
    path('vprasanje/<int:pk>/zakleni', views.zakleni, name='zakleni'),
    path('vprasanje/<int:pk>/odkleni', views.odkleni, name='odkleni'),
    path('moja_vprasanja', views.moja_vprasanja, name='moja_vprasanja'),
    path('registracija', views.registracija, name='registracija'),
    path('vpis', views.vpis.as_view(), name='vpis'),
    path('izpis', LogoutView.as_view(next_page='/'), name='izpis'),
    path('upload', views.upload, name='upload'),
    path('pregled_vprasanj', views.pregled_vprasanj, name='pregled_vprasanj'),
    path('ucenci/pregled', views.pregled_ucencev, name='pregled_ucencev'),
    path('ucenec/<int:pk>/odgovori', views.odgovori_ucenca, name='odgovori_ucenca'),
    path('ucenci/<int:pk>/vprasanja', views.vprasanja_ucenca, name='vprasanja_ucenca'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)