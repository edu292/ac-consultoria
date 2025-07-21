from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Geoloc
from .serializers import GeolocSerializer

@api_view(['GET'])
def geoloc_list_view(request):
    queryset = Geoloc.objects.all()

    month = request.query_params.get('month')
    year = request.query_params.get('year')

    if month:
        queryset = queryset.filter(date__month=month)

    if year:
        queryset = queryset.filter(date__year=year)

    serializer = GeolocSerializer(queryset, many=True)

    return Response(serializer.data)