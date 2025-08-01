from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.models import FurtoEquipamento
from .serializers import FurtoEquipamentoSerializer

@login_required
@api_view(['GET'])
def furto_equipamento_list(request):
    queryset = FurtoEquipamento.objects.filter(status=FurtoEquipamento.Status.VERIFICADO)

    month = request.query_params.get('month')
    year = request.query_params.get('year')

    if month:
        queryset = queryset.filter(data_ocorrencia__month=month)

    if year:
        queryset = queryset.filter(data_ocorrencia__year=year)

    serializer = FurtoEquipamentoSerializer(queryset, many=True)

    return Response(serializer.data)

@login_required
@api_view(['GET'])
def fetch_latest_period(request):
    latest_date_result = FurtoEquipamento.objects.filter(
        status=FurtoEquipamento.Status.VERIFICADO
    ).aggregate(latest_date=Max('data_ocorrencia'))

    latest_date = latest_date_result.get('latest_date')
    response_data = {
        'month': latest_date.month,
        'year': latest_date.year
    }

    return Response(response_data)

@staff_member_required
@api_view(['PATCH'])
def update_furto_equipamento(request, pk):
    instance = get_object_or_404(FurtoEquipamento, pk=pk)

    serializer = FurtoEquipamentoSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)