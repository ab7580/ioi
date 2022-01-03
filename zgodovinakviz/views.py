from django.shortcuts import render, get_object_or_404, redirect
from .models import Vprasanje, Uporabnik, PrikazanaVprasanja, Odgovor, Level, Slika
from .forms import VprasanjeForm, OdgovorForm, VprasanjeEditForm, RegistracijaForm, VpisForm, SlikaForm
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

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
    return render(request, 'zgodovinakviz/index.html', {'title': 'Dobrodošli v kvizkotu', 'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def upload(request):
    if Uporabnik.objects.get(user=request.user).locked:
        return redirect("kviz")
    if request.method == "POST":
        slika = request.FILES['slika']
        Slika.objects.create(slika=slika)
        return HttpResponse(status=201)
    return HttpResponse(status=500)

@login_required
def dodaj(request):
    if Uporabnik.objects.get(user=request.user).locked:
        return redirect("kviz")
    if request.method == "POST":
        form = VprasanjeForm(request.POST)
        if form.is_valid():
            vprasanje = form.save(commit=False)
            user = request.user
            vprasanje.author = Uporabnik.objects.get(user=user)
            print(vprasanje.slika_name)
            vprasanje.slika = Slika.objects.filter(slika__contains=vprasanje.slika_name)[0]
            vprasanje.published_date = timezone.now()
            vprasanje.save()
            return redirect('moja_vprasanja')
    else:
        form = VprasanjeForm()
        slikaForm = SlikaForm()
        return render(request, 'zgodovinakviz/add_question.html', {'form': form, 'title': 'Dodaj vprašanje', 'slikaForm': slikaForm, 'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def uredi(request, pk):
    if Uporabnik.objects.get(user=request.user).locked:
        return redirect("kviz")
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    if request.method == "POST":
        form = VprasanjeEditForm(request.POST, request.FILES, instance=vprasanje)
        if form.is_valid():
            vprasanje = form.save(commit=False)
            user = request.user
            vprasanje.author = Uporabnik.objects.get(user=user)
            vprasanje.slika = Slika.objects.filter(slika__contains=vprasanje.slika_name)[0]
            vprasanje.published_date = timezone.now()
            vprasanje.save()
            return redirect('moja_vprasanja')
    else:
        form = VprasanjeEditForm(instance=vprasanje)

    slikaForm = SlikaForm(instance=vprasanje.slika)
    slika = vprasanje.slika
    return render(request, 'zgodovinakviz/edit_question.html', {'form': form,
                                                                'vprasanje_pk': pk,
                                                                'title': 'Uredi vprašanje',
                                                                'uporabnik': Uporabnik.objects.get(user=request.user),
                                                                'slikaForm': slikaForm,
                                                                'slika': slika})

@login_required
def odstrani(request, pk):
    if Uporabnik.objects.get(user=request.user).locked:
        return redirect("kviz")
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    vprasanje.slika.delete()
    vprasanje.delete()
    return redirect('moja_vprasanja')

@login_required
def zakleni(request, pk):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    vprasanje.locked = True
    vprasanje.save()
    return redirect('pregled_vprasanj')

@login_required
def odkleni(request, pk):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    vprasanje.locked = False
    vprasanje.save()
    return redirect('pregled_vprasanj')

@login_required
def vprasanje(request, pk):
    vprasanje = get_object_or_404(Vprasanje, pk=pk)
    uporabnik = Uporabnik.objects.get(user=request.user)
    odgovorjeno = Odgovor.objects.filter(author=uporabnik, vprasanje=vprasanje)
    if odgovorjeno:
        return redirect("kviz")

    if request.method == "POST":
        user = request.user
        if vprasanje.pravilen_odgovor in request.POST:
            Odgovor.objects.create(author = Uporabnik.objects.get(user=user),
                                   vprasanje = vprasanje,
                                   izbran_odgovor = vprasanje.pravilen_odgovor,
                                   pravilen = True,
                                   published_date = timezone.now())
            return render(request, 'zgodovinakviz/question.html',
                          {'vprasanje': vprasanje, 'title': 'Vprasanje', 'success': True, 'pravilen': True, 'uporabnik': Uporabnik.objects.get(user=request.user)})
        elif vprasanje.napacen_odgovor_1 in request.POST:
            Odgovor.objects.create(author = Uporabnik.objects.get(user=user),
                                   vprasanje = vprasanje,
                                   izbran_odgovor = vprasanje.napacen_odgovor_1,
                                   pravilen = False,
                                   published_date = timezone.now())
            return render(request, 'zgodovinakviz/question.html',
                          {'vprasanje': vprasanje, 'title': 'Vprasanje', 'success': True,
                           'pravilen': False, 'uporabnik': Uporabnik.objects.get(user=request.user)})
        elif vprasanje.napacen_odgovor_2 in request.POST:
            Odgovor.objects.create(author = Uporabnik.objects.get(user=user),
                                   vprasanje = vprasanje,
                                   izbran_odgovor = vprasanje.napacen_odgovor_2,
                                   pravilen = False,
                                   published_date = timezone.now())
            return render(request, 'zgodovinakviz/question.html',
                          {'vprasanje': vprasanje, 'title': 'Vprasanje', 'success': True,
                           'pravilen': False, 'uporabnik': Uporabnik.objects.get(user=request.user)})

    else:
        form = OdgovorForm()
        return render(request, 'zgodovinakviz/question.html', {'form':form,
                                                               'vprasanje': vprasanje,
                                                               'title': vprasanje.vprasanje,
                                                               'success': False, 'pravilen': False,
                                                               'uporabnik': Uporabnik.objects.get(user=request.user)})

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
        """while chosen in chosen_ints:
            chosen = random.randint(0, len(neodgovorjena_vprasanja) - 1)"""
        chosen_ints.append(chosen)
        chosen_vprasanje = neodgovorjena_vprasanja[chosen]
        neodgovorjena_vprasanja.remove(chosen_vprasanje)
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
                                                                'title': 'Seznam vprašanj',
                                                                'stopnja': uporabnik.level.ime,
                                                                'napredovanje': 6-len(pravilna_vprasanja),
                                                                'nova_stopnja': nova_stopnja,
                                                                'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def moja_vprasanja(request):
    vprasanja = Vprasanje.objects.filter(author=Uporabnik.objects.get(user=request.user)).order_by('-created_date')
    return render(request, 'zgodovinakviz/questions_overview.html', {'vprasanja': vprasanja,
                                                                     'title': 'Moja vprašanja',
                                                                     'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def pregled_vprasanj(request):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    vprasanja = Vprasanje.objects.all().order_by('-created_date')
    return render(request, 'zgodovinakviz/questions_overview_ucitelj.html', {'vprasanja': vprasanja,
                                                                     'title': 'Pregled vprašanj',
                                                                     'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def pregled_ucencev(request):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    ucenci = Uporabnik.objects.filter(ucitelj=False)
    return render(request, 'zgodovinakviz/students_overview.html', {'ucenci': ucenci,
                                                                     'title': 'Pregled učencev',
                                                                     'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def odgovori_ucenca(request, pk):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    ucenec = get_object_or_404(Uporabnik, pk=pk)
    odgovori = Odgovor.objects.filter(author=ucenec)
    return render(request, 'zgodovinakviz/students_answers.html', {'ucenec': ucenec,
                                                                   'odgovori': odgovori,
                                                                    'title': 'Pregled odgovorov učenca',
                                                                    'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def vprasanja_ucenca(request, pk):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    ucenec = get_object_or_404(Uporabnik, pk=pk)
    vprasanja = Vprasanje.objects.filter(author=ucenec).order_by('-created_date')
    return render(request, 'zgodovinakviz/questions_overview_ucitelj_en.html', {'ucenec': ucenec,
                                                                   'vprasanja': vprasanja,
                                                                    'title': 'Pregled vprašanj učenca',
                                                                    'uporabnik': Uporabnik.objects.get(user=request.user)})

@login_required
def zakleni_ucenca(request, pk):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    ucenec = get_object_or_404(Uporabnik, pk=pk)
    ucenec.locked = True
    ucenec.save()
    return redirect('pregled_ucencev')

@login_required
def odkleni_ucenca(request, pk):
    if not Uporabnik.objects.get(user=request.user).ucitelj:
        return redirect("kviz")
    ucenec = get_object_or_404(Uporabnik, pk=pk)
    ucenec.locked = False
    ucenec.save()
    return redirect('pregled_ucencev')

