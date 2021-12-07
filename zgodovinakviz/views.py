from django.shortcuts import render

def vprasanja(request):
    return render(request, 'zgodovinakviz/question_list.html', {})
