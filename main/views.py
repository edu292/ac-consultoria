from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ocorrencia

@login_required()
def powerbi(request):
    return render(request, 'main/powerbi.html')

@login_required()
def mapacalor(request):
    return render(request, 'main/mapa_calor.html')

@login_required()
def index(request):
    return render(request, 'main/index.html')

@login_required()
def double_checker(request):
    if request.htmx.trigger_name:
        field = request.htmx.trigger_name
        search = {f'{field}__unaccent__icontains': request.GET.get(field)}
        context = {'ocorrencias': Ocorrencia.objects.filter(**search)[:6]}
        return render(request, 'main/double_checker.html#results', context)
    return render(request, 'main/double_checker.html')