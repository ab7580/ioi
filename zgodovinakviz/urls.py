from django.urls import path
from . import views

urlpatterns = [
    path('', views.vpis, name='vpis'),
    path('vstop', views.vstopi, name='vstopi'),
    path('kviz', views.kviz, name='kviz'),
    path('dodaj', views.dodaj, name='dodaj'),
    path('uredi/<int:pk>', views.uredi, name='uredi'),
    path('vprasanje/<int:pk>', views.vprasanje, name='vprasanje'),
    path('moja_vprasanja', views.moja_vprasanja, name='moja_vprasanja'),
]