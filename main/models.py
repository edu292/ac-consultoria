from django.db import models

class Ocorrencia(models.Model):
    ESTRUTURA_CRIMINAL_CHOICES = (
        ('OPORTUNISTA', 'Oportunista'),
        ('RECEPTACAO', 'Receptação'),
        ('QUADRILHA', 'Quadrilha')
    )

    nome = models.CharField(max_length=100)
    numero_documento =  models.CharField(max_length=100, null=True, blank=True)
    numero_bo = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100)
    placa = models.CharField(max_length=100, null=True, blank=True)
    delito = models.CharField(max_length=100)
    data = models.DateField()
    estrutura_criminal = models.CharField(max_length=11, choices=ESTRUTURA_CRIMINAL_CHOICES)

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"

    def __str__(self):
        return self.nome


class FurtoEquipamento(models.Model):
    class Status(models.TextChoices):
        AGUARDANDO_GEO = 'AGUARDANDO_GEO', 'Aguardando Geocodificação'
        GEO_FALHOU = 'GEO_FALHOU', 'Falha na Geocodificação'
        AGUARDANDO_VERIFICACAO = 'AGUARDANDO_VERIFICACAO', 'Aguardando Verificação'
        VERIFICADO = 'VERIFICADO', 'Verificado'

    data_ocorrencia = models.DateField(verbose_name="Data da Ocorrência",
                                       db_index=True)

    status = models.CharField(max_length=22,
                              choices=Status.choices,
                              default=Status.AGUARDANDO_GEO,
                              db_index=True)

    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=30, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2, verbose_name='UF', default='PR')
    tipo_de_equipamento = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Furto de Equipamento'
        verbose_name_plural = 'Furtos de Equipamento'

    def __str__(self):
        return f"{self.tipo_de_equipamento} em {self.cidade}/{self.uf} - {self.get_status_display()}"