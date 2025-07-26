from django.contrib import admin
from .models import Ocorrencia
from import_export.admin import ImportExportModelAdmin
from .resources import OcorrenciaResource

@admin.register(Ocorrencia)
class BookAdmin(ImportExportModelAdmin):
    resource_class = OcorrenciaResource