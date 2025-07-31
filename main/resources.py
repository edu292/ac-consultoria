from import_export import resources, widgets
from import_export.fields import Field
from .models import Ocorrencia, FurtoEquipamento
import re

class EstruturaCriminalWidget(widgets.Widget):
    def __init__(self, choices):
        super().__init__(self)
        self.choices = choices

    def clean(self, value, row=None, **kwargs):
        if value is None:
            return None

        for db_value, display_value in self.choices:
            if db_value or display_value.upper() in value.upper():
                return db_value

        raise ValueError(f'A estrutura criminal: {value} não está entre as opções válidas: {self.choices}')

class OcorrenciaResource(resources.ModelResource):
    data = Field(attribute='data', column_name='Data ', widget=widgets.DateWidget())
    cidade = Field(attribute='cidade', column_name='Cidade')
    nome = Field(attribute='nome', column_name='Nome Indiciado')
    numero_bo = Field(attribute='numero_bo', column_name='Nº do B.O')
    numero_documento = Field(attribute='numero_documento', column_name='numero ')
    placa = Field(attribute='placa', column_name='placa')
    delito = Field(attribute='delito', column_name='Indiciado por :')
    estrutura_criminal = Field(attribute='estrutura_criminal', column_name='TIPO EXTRUTURA ',
                               widget=EstruturaCriminalWidget(Ocorrencia.ESTRUTURA_CRIMINAL_CHOICES))

    class Meta:
        model = Ocorrencia
        import_id_fields = ('numero_bo',)
        skip_unchanged = True
        exclude = ('id',)


class NumeroWidget(widgets.CharWidget):
    def __init__(self):
        super().__init__(allow_blank=False)

    def clean(self, value, row=None, **kwargs):
        cleaned_value = super().clean(value, row, **kwargs)
        if cleaned_value is None:
            return None

        processing_value = cleaned_value.split('-')[0]
        final_number = re.sub(r'\D', '', processing_value)
        return final_number if final_number else None


class TitleCaseWidget(widgets.CharWidget):
    def __init__(self):
        super().__init__(allow_blank=False)
    
    def clean(self, value, row=None, **kwargs):
        cleaned_value = super().clean(value, row, **kwargs)
        if cleaned_value is not None:
            return cleaned_value.strip().title()
        return None


class FurtoEquipamentoResource(resources.ModelResource):
    data_ocorrencia = Field(attribute='data_ocorrencia', column_name='Data',
                            widget=widgets.DateWidget(format='%d/%m/%Y',coerce_to_string=False))
    logradouro = Field(attribute='logradouro', column_name='Rua, AV, Logradouro', widget=TitleCaseWidget())
    numero = Field(attribute='numero', column_name='Nº', widget=NumeroWidget())
    bairro = Field(attribute='bairro', column_name='Bairro', widget=TitleCaseWidget())
    cidade = Field(attribute='cidade', column_name='Cidade', widget=TitleCaseWidget())
    uf = Field(attribute='uf', column_name='UF')
    tipo_de_equipamento = Field(attribute='tipo_de_equipamento', column_name='Tipo de cabo', widget=TitleCaseWidget())

    class Meta:
        model = FurtoEquipamento
        import_id_fields = ()
        fields = ('data_ocorrencia', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'tipo_de_equipamento')