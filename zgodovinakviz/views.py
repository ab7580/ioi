from django.shortcuts import render, get_object_or_404, redirect
from .models import Vprasanje, Uporabnik, PrikazanaVprasanja
from .forms import VprasanjeForm
from django.utils import timezone
from django.contrib.auth import authenticate

import random

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
    if request.method == "POST":
        form = VprasanjeForm(request.POST)
        if form.is_valid():
            vprasanje = form.save(commit=False)
            user = request.user
            vprasanje.author = Uporabnik.objects.get(user=user)
            vprasanje.published_date = timezone.now()
            vprasanje.save()
            return redirect('moja_vprasanja')
    else:
        form = VprasanjeForm()
        return render(request, 'zgodovinakviz/add_question.html', {'form': form})

def uredi(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    if request.method == "POST":
        form = VprasanjeForm(request.POST, instance=vprasanje)
        if form.is_valid():
            vprasanje = form.save(commit=False)
            user = request.user
            vprasanje.author = Uporabnik.objects.get(user=user)
            vprasanje.published_date = timezone.now()
            vprasanje.save()
            return redirect('moja_vprasanja')
    else:
        form = VprasanjeForm(instance=vprasanje)
    return render(request, 'zgodovinakviz/edit_question.html', {'form': form})

def odstrani(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    vprasanje.delete()
    return redirect('moja_vprasanja')

def vprasanje(request):
    return render(request, 'zgodovinakviz/question.html', {})

def generateNewVprasanjaForUser(uporabnik, prikazanaVprasanja):
    odgovorjena_vprasanja = Odgovor.objects.filter(uporabnik=uporabnik).values('vprasanje__id')
    neodgovorjena_vprasanja = Vprasanje.objects.exclude(pk__in=odgovorjena_vprasanja).values_list('pk')

    chosen_ints = []
    chosen_pks = []
    for i in range(9):
        chosen = random.randint(0, len(neodgovorjena_vprasanja) - 1)
        if chosen not in chosen_ints:
            chosen_ints.append(chosen)
            chosen_vprasanje = neodgovorjena_vprasanja[chosen]
            chosen_pks.append(chosen_vprasanje)
            PrikazanaVprasanja.create(uporabnik=uporabnik, vprasanje=chosen_vprasanje)

    return Vprasanje.objects.filter(pk__in=chosen_pks)

def kviz(request):
    user = request.user
    uporabnik = Uporabnik.objects.get(user=user)
    prikazanaVprasanja = PrikazanaVprasanja.objects.filter(uporabnik=uporabnik)
    if len(prikazanaVprasanja) != 9:
        prikazanaVprasanja = generateNewVprasanjaForUser(uporabnik, prikazanaVprasanja)
    return render(request, 'zgodovinakviz/question_list.html', {'vprasanja': prikazanaVprasanja})

def moja_vprasanja(request):
    vprasanja = Vprasanje.objects.all().order_by('created_date');
    return render(request, 'zgodovinakviz/questions_overview.html', {'vprasanja': vprasanja})

