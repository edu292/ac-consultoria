from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

@login_required()
def powerbi(request):
    return render(request, 'main/powerbi.html')

@login_required()
def mapacalor(request):
    return render(request, 'main/mapa_calor.html')

def index(request):
    return redirect(reverse('main:powerbi'))