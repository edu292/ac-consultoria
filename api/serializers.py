from rest_framework import serializers

from .models import Geoloc

class GeolocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geoloc
        fields = ['date', 'latitude', 'longitude', 'type']