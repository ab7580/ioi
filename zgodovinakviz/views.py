from django.shortcuts import render, get_object_or_404, redirect
from .models import Vprasanje, Uporabnik, PrikazanaVprasanja, Odgovor, Level
from .forms import VprasanjeForm, OdgovorForm, VprasanjeEditForm, RegistracijaForm, VpisForm
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

import random

def start(request):
    return render(request, 'zgodovinakviz/unauthenticated.html', {})

def registracija(request):
    if request.method == "POST":
        form = RegistracijaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Uporabnik.objects.create(user=user, level=Level.objects.get(vrstni_red=1))
            return redirect("vstopi")
        else:
            return render(request, 'zgodovinakviz/register.html', {'form': form})
    else:
        form = RegistracijaForm()
        return render(request, 'zgodovinakviz/register.html', {'form': form})

class vpis(LoginView):
    template_name = "zgodovinakviz/login.html"
    next_page = "vstop"
    authentication_form = VpisForm

    """
def vpis(request):
    if request.method == "POST":
        form = VpisForm(request.POST)
        if form.is_valid():
            print("valid")
            login(request, user)
            return redirect("vstopi")
        else:
            return render(request, 'zgodovinakviz/login.html', {'form': form})
    else:
        form = VpisForm()
        return render(request, 'zgodovinakviz/login.html', {'form': form})"""

    """user = authenticate(username='john', password='secret')
        if user is not None:
        # A backend authenticated the credentials
        else:
        # No backend authenticated the credentials"""

@login_required
def vstopi(request):
    return render(request, 'zgodovinakviz/index.html', {'title': 'Dobrodosli v kvizkotu'})

@login_required
def dodaj(request):
    if request.method == "POST":
        form = VprasanjeForm(request.POST, request.FILES)
        if form.is_valid():
            vprasanje = form.save(commit=False)
            user = request.user
            vprasanje.author = Uporabnik.objects.get(user=user)
            vprasanje.published_date = timezone.now()
            vprasanje.save()
            return redirect('moja_vprasanja')
    else:
        form = VprasanjeForm()
        return render(request, 'zgodovinakviz/add_question.html', {'form': form, 'title': 'Dodaj vprasanje'})

@login_required
def uredi(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    if request.method == "POST":
        form = VprasanjeEditForm(request.POST, request.FILES, instance=vprasanje)
        if form.is_valid():
            vprasanje = form.save(commit=False)
            user = request.user
            vprasanje.author = Uporabnik.objects.get(user=user)
            vprasanje.published_date = timezone.now()
            vprasanje.save()
            return redirect('moja_vprasanja')
    else:
        form = VprasanjeEditForm(instance=vprasanje)
    return render(request, 'zgodovinakviz/edit_question.html', {'form': form, 'vprasanje_pk': pk, 'title': 'Uredi vprasanje'})

@login_required
def odstrani(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    vprasanje.delete()
    return redirect('moja_vprasanja')

@login_required
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
        elif vprasanje.napacen_odgovor_2 in request.POST:
            Odgovor.objects.create(author = Uporabnik.objects.get(user=user),
                                   vprasanje = vprasanje,
                                   izbran_odgovor = vprasanje.napacen_odgovor_2,
                                   pravilen = False,
                                   published_date = timezone.now())
        return redirect('kviz')
    else:
        form = OdgovorForm()
    return render(request, 'zgodovinakviz/question.html', {'form':form, 'vprasanje': vprasanje, 'title': 'Vprasanje'})

@login_required
def izbrisiPrikazanaVprasanjaForUser(uporabnik):
    prikazanaVprasanja = PrikazanaVprasanja.objects.filter(uporabnik=uporabnik)
    prikazanaVprasanja.delete()

@login_required
def generateNewVprasanjaForUser(uporabnik, num):
    odgovorjena_vprasanja = Odgovor.objects.filter(author=uporabnik).values('vprasanje__id')
    neodgovorjena_vprasanja = Vprasanje.objects.exclude(pk__in=odgovorjena_vprasanja).values('pk')
    neodgovorjena_vprasanja = [v['pk'] for v in neodgovorjena_vprasanja]

    chosen_ints = []
    chosen_pks = []
    for i in range(num):
        if len(neodgovorjena_vprasanja) == 0:
            break
        chosen = random.randint(0, len(neodgovorjena_vprasanja) - 1)
        while chosen in chosen_ints:
            chosen = random.randint(0, len(neodgovorjena_vprasanja) - 1)
        chosen_ints.append(chosen)
        chosen_vprasanje = neodgovorjena_vprasanja[chosen]
        chosen_pks.append(chosen_vprasanje)
        PrikazanaVprasanja.objects.create(uporabnik=uporabnik, vprasanje=Vprasanje.objects.get(pk=chosen_vprasanje))

@login_required
def prikaziVprasanjaForUser(uporabnik):
    prikazanaVprasanja = PrikazanaVprasanja.objects.filter(uporabnik=uporabnik)
    if len(prikazanaVprasanja) != 9:
        generateNewVprasanjaForUser(uporabnik, 9 - len(prikazanaVprasanja))
        prikazanaVprasanja = PrikazanaVprasanja.objects.filter(uporabnik=uporabnik)
        prikazanaVprasanja = Vprasanje.objects.filter(
            pk__in=[v['vprasanje'] for v in prikazanaVprasanja.values('vprasanje')])
    else:
        prikazanaVprasanja = Vprasanje.objects.filter(
            pk__in=[v['vprasanje'] for v in prikazanaVprasanja.values('vprasanje')])

    odgovorjena_vprasanja = Odgovor.objects.filter(author=uporabnik, vprasanje__in=prikazanaVprasanja)
    neodgovorjena_vprasanja = prikazanaVprasanja.exclude(
        pk__in=[v['vprasanje__id'] for v in odgovorjena_vprasanja.values('vprasanje__id')]).values('pk')
    neodgovorjena_vprasanja = [v['pk'] for v in neodgovorjena_vprasanja]
    pravilna_vprasanja = odgovorjena_vprasanja.filter(pravilen=True).values('vprasanje__id')
    pravilna_vprasanja = [v['vprasanje__id'] for v in pravilna_vprasanja]
    napacna_vprasanja = odgovorjena_vprasanja.filter(pravilen=False).values('vprasanje__id')
    napacna_vprasanja = [v['vprasanje__id'] for v in napacna_vprasanja]

    return prikazanaVprasanja, neodgovorjena_vprasanja, pravilna_vprasanja, napacna_vprasanja

@login_required
def kviz(request):
    user = request.user
    uporabnik = Uporabnik.objects.get(user=user)
    prikazanaVprasanja, neodgovorjena_vprasanja, pravilna_vprasanja, napacna_vprasanja = prikaziVprasanjaForUser(uporabnik)

    nova_stopnja = 0
    # če je pravilno odgovoril 6 ali več, gre na drugo stopnjo
    if len(pravilna_vprasanja) >= 6:
        nova_stopnja = 1
        if uporabnik.level.vrstni_red == 4:
            nova_stopnja = 2
        else:
            nov_level = Level.objects.get(vrstni_red = uporabnik.level.vrstni_red + 1)
            uporabnik.level = nov_level
            uporabnik.save()
        izbrisiPrikazanaVprasanjaForUser(uporabnik)
        prikazanaVprasanja, neodgovorjena_vprasanja, pravilna_vprasanja, napacna_vprasanja = prikaziVprasanjaForUser(uporabnik)

    # če je napačno odgovoril na več kot 3 vprašanja, ne more več napredovati na naslednjo stopnjo
    if len(napacna_vprasanja) >= 3:
        nova_stopnja = -1
        izbrisiPrikazanaVprasanjaForUser(uporabnik)
        prikazanaVprasanja, neodgovorjena_vprasanja, pravilna_vprasanja, napacna_vprasanja = prikaziVprasanjaForUser(uporabnik)

    return render(request, 'zgodovinakviz/question_list.html', {'vprasanja1': prikazanaVprasanja[0:3],
                                                                'vprasanja2': prikazanaVprasanja[3:6],
                                                                'vprasanja3': prikazanaVprasanja[6:9],
                                                                'pravilna': pravilna_vprasanja,
                                                                'napacna': napacna_vprasanja,
                                                                'neodgovorjena': neodgovorjena_vprasanja,
                                                                'title': 'Seznam vprasanj',
                                                                'stopnja': uporabnik.level.ime,
                                                                'napredovanje': 6-len(pravilna_vprasanja),
                                                                'nova_stopnja': nova_stopnja})

@login_required
def moja_vprasanja(request):
    vprasanja = Vprasanje.objects.all().order_by('-created_date');
    return render(request, 'zgodovinakviz/questions_overview.html', {'vprasanja': vprasanja, 'title': 'Moja vprasanja'})

