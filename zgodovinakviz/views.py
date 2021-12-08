from django.shortcuts import render
from .models import Vprasanje

def vpis(request):
    return render(request, 'zgodovinakviz/unauthenticated.html', {})

def vstopi(request):
    return render(request, 'zgodovinakviz/index.html', {})

def dodaj(request):
    return render(request, 'zgodovinakviz/add_question.html', {})

def uredi(request):
    return render(request, 'zgodovinakviz/edit_question.html', {})

def vprasanje(request):
    return render(request, 'zgodovinakviz/question.html', {})

def kviz(request):
    return render(request, 'zgodovinakviz/question_list.html', {})

def moja_vprasanja(request):
    vprasanja = Vprasanje.objects.all().order_by('created_date');
    return render(request, 'zgodovinakviz/questions_overview.html', {'vprasanja': vprasanja})

