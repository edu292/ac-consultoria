from django.contrib import admin
from .models import Ocorrencia
from import_export.admin import ImportExportModelAdmin
from .resources import OcorrenciaResource

@admin.register(Ocorrencia)
class BookAdmin(ImportExportModelAdmin):
    resource_class = OcorrenciaResource
    list_display = [field.name for field in Ocorrencia._meta.fields if not field.primary_key]
    list_editable = [field.name for field in Ocorrencia._meta.fields if not field.primary_key]
    list_display_links = None
    search_fields = ['nome', 'placa', 'numero_documento']