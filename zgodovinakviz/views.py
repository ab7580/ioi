from django.shortcuts import render, get_object_or_404, redirect
from .models import Vprasanje, Uporabnik, PrikazanaVprasanja, Odgovor
from .forms import VprasanjeForm, OdgovorForm, VprasanjeEditForm
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
        form = VprasanjeEditForm(request.POST, instance=vprasanje)
        if form.is_valid():
            vprasanje = form.save(commit=False)
            user = request.user
            vprasanje.author = Uporabnik.objects.get(user=user)
            vprasanje.published_date = timezone.now()
            vprasanje.save()
            return redirect('moja_vprasanja')
    else:
        form = VprasanjeEditForm(instance=vprasanje)
    return render(request, 'zgodovinakviz/edit_question.html', {'form': form, 'vprasanje_pk': pk})

def odstrani(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    vprasanje.delete()
    return redirect('moja_vprasanja')

def vprasanje(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    if request.method == "POST":
        user = request.user
        if vprasanje.pravilen_odgovor in request.POST:
            Odgovor.objects.create(author = Uporabnik.objects.get(user=user),
                                   vprasanje = vprasanje,
                                   izbran_odgovor = vprasanje.pravilen_odgovor,
                                   pravilen = True,
                                   published_date = timezone.now())
        elif vprasanje.napacen_odgovor_1 in request.POST:
            Odgovor.objects.create(author = Uporabnik.objects.get(user=user),
                                   vprasanje = vprasanje,
                                   izbran_odgovor = vprasanje.napacen_odgovor_1,
                                   pravilen = False,
                                   published_date = timezone.now())
        elif vprasanje.napacen_odgovor_1 in request.POST:
            Odgovor.objects.create(author = Uporabnik.objects.get(user=user),
                                   vprasanje = vprasanje,
                                   izbran_odgovor = vprasanje.napacen_odgovor_2,
                                   pravilen = False,
                                   published_date = timezone.now())
        return redirect('kviz')
    else:
        form = OdgovorForm()
    return render(request, 'zgodovinakviz/question.html', {'form':form, 'vprasanje': vprasanje})

def generateNewVprasanjaForUser(uporabnik, prikazanaVprasanja):
    odgovorjena_vprasanja = Odgovor.objects.filter(author=uporabnik).values('vprasanje__id')
    neodgovorjena_vprasanja = Vprasanje.objects.exclude(pk__in=odgovorjena_vprasanja).values('pk')
    neodgovorjena_vprasanja = [v['pk'] for v in neodgovorjena_vprasanja]

    chosen_ints = []
    chosen_pks = []
    for i in range(9):
        chosen = random.randint(0, len(neodgovorjena_vprasanja) - 1)
        while chosen in chosen_ints:
            chosen = random.randint(0, len(neodgovorjena_vprasanja) - 1)
        chosen_ints.append(chosen)
        chosen_vprasanje = neodgovorjena_vprasanja[chosen]
        print(chosen_vprasanje)
        chosen_pks.append(chosen_vprasanje)
        PrikazanaVprasanja.objects.create(uporabnik=uporabnik, vprasanje=Vprasanje.objects.get(pk=chosen_vprasanje))

    return Vprasanje.objects.filter(pk__in=chosen_pks)

def kviz(request):
    user = request.user
    uporabnik = Uporabnik.objects.get(user=user)
    prikazanaVprasanja = PrikazanaVprasanja.objects.filter(uporabnik=uporabnik)
    print([v['pk'] for v in prikazanaVprasanja.values('pk')])
    if len(prikazanaVprasanja) != 9:
        prikazanaVprasanja = generateNewVprasanjaForUser(uporabnik, prikazanaVprasanja)
    else:
        prikazanaVprasanja = Vprasanje.objects.filter(pk__in = [v['vprasanje'] for v in prikazanaVprasanja.values('vprasanje')])

    pravilno_odgovorjena_vprasanja = Odgovor.objects.filter(author=uporabnik, vprasanje__in=prikazanaVprasanja).values('vprasanje__id')
    print(pravilno_odgovorjena_vprasanja)
    pravilno_odgovorjena_vprasanja = [v['vprasanje__id'] for v in pravilno_odgovorjena_vprasanja]
    print(prikazanaVprasanja)
    return render(request, 'zgodovinakviz/question_list.html', {'vprasanja1': prikazanaVprasanja[0:3],
                                                                'vprasanja2': prikazanaVprasanja[3:6],
                                                                'vprasanja3': prikazanaVprasanja[6:9],
                                                                'pravilna': pravilno_odgovorjena_vprasanja})

def moja_vprasanja(request):
    vprasanja = Vprasanje.objects.all().order_by('-created_date');
    return render(request, 'zgodovinakviz/questions_overview.html', {'vprasanja': vprasanja})

