from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Prisoes

@login_required()
def powerbi(request):
    if request.htmx:
        return render(request, 'main/powerbi.html#htmx')
    return render(request, 'main/powerbi.html')

@login_required()
def mapacalor(request):
    return render(request, 'main/mapa_calor.html')

def index(request):
    return redirect(reverse('main:powerbi'))

@login_required()
def double_checker(request):
    if request.htmx:
        if request.headers.get('HX-Trigger'):
            field = request.headers.get('HX-Trigger-Name')
            search = {f'{field}__icontains': request.GET.get(field)}
            context = {'prisoes': Prisoes.objects.filter(**search)[:6]}
            return render(request, 'main/double_checker.html#results', context)
        return render(request, 'main/double_checker.html#htmx')
    return render(request, 'main/double_checker.html')