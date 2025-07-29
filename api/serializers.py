from rest_framework import serializers

from main.models import FurtoEquipamento

class FurtoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurtoEquipamento
        fields = ['data_ocorrencia', 'latitude', 'longitude', 'tipo_de_equipamento']