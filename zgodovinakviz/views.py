from django.shortcuts import render, get_object_or_404
from .models import Vprasanje
from .forms import VprasanjeForm

from django.contrib.auth import authenticate

def start(request):
    return render(request, 'zgodovinakviz/unauthenticated.html', {})

def registracija(request):
    return render(request, 'zgodovinakviz/register.html', {})

def vpis(request):
    """user = authenticate(username='john', password='secret')
    if user is not None:
    # A backend authenticated the credentials
    else:
    # No backend authenticated the credentials"""
    return render(request, 'zgodovinakviz/login.html', {})

def vstopi(request):
    return render(request, 'zgodovinakviz/index.html', {})

def dodaj(request):
    form = VprasanjeForm()
    return render(request, 'zgodovinakviz/add_question.html', {'form': form})

def uredi(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    return render(request, 'zgodovinakviz/edit_question.html', {'vprasanje': vprasanje})

def vprasanje(request):
    return render(request, 'zgodovinakviz/question.html', {})

def kviz(request):
    return render(request, 'zgodovinakviz/question_list.html', {})

def moja_vprasanja(request):
    vprasanja = Vprasanje.objects.all().order_by('created_date');
    return render(request, 'zgodovinakviz/questions_overview.html', {'vprasanja': vprasanja})

