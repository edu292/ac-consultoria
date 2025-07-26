from import_export import resources, fields, widgets
from .models import Ocorrencia

class EstruturaCriminalWidget(widgets.Widget):
    def __init__(self, choices):
        super().__init__(self)
        self.choices = choices

    def clean(self, value, row=None, **kwargs):
        if value is None:
            return None

        for db_value, display_value in self.choices:
            if db_value or display_value.upper() in value:
                return db_value

        raise ValueError(f'A estrutura criminal: {value} não está entre as opções válidas: {self.choices}')

class OcorrenciaResource(resources.ModelResource):
    data = fields.Field(attribute='data', column_name='Data ', widget=widgets.DateWidget())
    cidade = fields.Field(attribute='cidade', column_name='Cidade')
    nome = fields.Field(attribute='nome', column_name='Nome Indiciado')
    numero_bo = fields.Field(attribute='numero_bo', column_name='Nº do B.O')
    numero_documento = fields.Field(attribute='numero_documento', column_name='numero ')
    placa = fields.Field(attribute='placa', column_name='placa')
    delito = fields.Field(attribute='delito', column_name='Indiciado por :')
    estrutura_criminal = fields.Field(attribute='estrutura_criminal', column_name='TIPO EXTRUTURA ',
                                      widget=EstruturaCriminalWidget(Ocorrencia.ESTRUTURA_CRIMINAL_CHOICES))

    class Meta:
        model = Ocorrencia
        import_id_fields = ('numero_bo',)
        skip_unchanged = True
        exclude = ('id',)