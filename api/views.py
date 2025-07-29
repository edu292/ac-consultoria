from django.db.models import Max

from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.models import FurtoEquipamento
from .serializers import FurtoEquipamentoSerializer

@api_view(['GET'])
def geoloc_list_view(request):
    queryset = FurtoEquipamento.objects.filter(status=FurtoEquipamento.Status.VERIFICADO)

    month = request.query_params.get('month')
    year = request.query_params.get('year')

    if month:
        queryset = queryset.filter(data_ocorrencia__month=month)

    if year:
        queryset = queryset.filter(data_ocorrencia__year=year)

    serializer = FurtoEquipamentoSerializer(queryset, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def latest_month(request):
    latest_date_result = FurtoEquipamento.objects.filter(
        status=FurtoEquipamento.Status.VERIFICADO
    ).aggregate(latest_date=Max('data_ocorrencia'))

    latest_date = latest_date_result.get('latest_date')
    response_data = {
        'latest_month': int(latest_date.strftime('%m'))
    }

    return Response(response_data)