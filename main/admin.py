from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from rangefilter.filters import DateRangeFilter
from import_export.admin import ImportExportModelAdmin
import json

from .models import Ocorrencia, FurtoEquipamento
from .resources import OcorrenciaResource, FurtoEquipamentoResource


@admin.register(Ocorrencia)
class OcorrenciaAdmin(ImportExportModelAdmin):
    resource_class = OcorrenciaResource
    list_display = [field.name for field in Ocorrencia._meta.fields if not field.primary_key]
    list_filter = ['estrutura_criminal', ('data', DateRangeFilter)]
    search_fields = ['nome', 'placa', 'numero_documento']


@admin.register(FurtoEquipamento)
class FurtoEquipamentoAdmin(ImportExportModelAdmin):
    resource_class = FurtoEquipamentoResource
    list_filter = ['status', ('data_ocorrencia', DateRangeFilter), 'tipo_de_equipamento', 'data_registro']
    ordering = ['-data_ocorrencia']
    date_hierarchy = 'data_ocorrencia'
    actions = ['verify_on_map']

    @admin.action(description="Verificar localizações selecionadas no mapa")
    def verify_on_map(self, request, queryset):
        selected_ids = ",".join(str(pk) for pk in queryset.values_list('pk', flat=True))

        url = reverse('admin:map_verification') + f'?ids={selected_ids}'

        return HttpResponseRedirect(url)

    def map_verification(self, request):
        selected_ids_str = request.GET.get('ids')
        if not selected_ids_str:
            locations = []
        else:
            selected_ids = [int(pk) for pk in selected_ids_str.split(',')]
            queryset = FurtoEquipamento.objects.filter(pk__in=selected_ids)
            locations = list(queryset.values(
                'id', 'latitude', 'longitude', 'logradouro', 'numero', 'bairro', 'cidade'
            ))

        return render(request, 'admin/map_verification.html', {'locations': locations})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('map-verification', self.admin_site.admin_view(self.map_verification), name='map_verification')
        ]

        return custom_urls + urls