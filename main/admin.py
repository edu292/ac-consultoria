from django.contrib import admin
from .models import Ocorrencia, FurtoEquipamento
from import_export.admin import ImportExportModelAdmin
from .resources import OcorrenciaResource, FurtoEquipamentoResource

@admin.register(Ocorrencia)
class OcorrenciaAdmin(ImportExportModelAdmin):
    resource_class = OcorrenciaResource
    list_display = [field.name for field in Ocorrencia._meta.fields if not field.primary_key]
    list_filter = ['estrutura_criminal']
    search_fields = ['nome', 'placa', 'numero_documento']

@admin.register(FurtoEquipamento)
class ModelNameAdmin(ImportExportModelAdmin):
    resource_class = FurtoEquipamentoResource
    list_filter = ['status', 'data_registro', 'tipo_de_equipamento']
    ordering = ['-data_ocorrencia']