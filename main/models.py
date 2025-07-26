from django.db import models

class Ocorrencia(models.Model):
    ESTRUTURA_CRIMINAL_CHOICES = (
        ('OPORTUNISTA', 'Oportunista'),
        ('RECEPTACAO', 'Receptação'),
        ('QUADRILHA', 'Quadrilha')
    )

    nome = models.CharField(max_length=100)
    numero_documento =  models.CharField(max_length=100, null=True)
    numero_bo = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100)
    placa = models.CharField(max_length=100, null=True)
    delito = models.CharField(max_length=100)
    data = models.DateField()
    estrutura_criminal = models.CharField(max_length=11, choices=ESTRUTURA_CRIMINAL_CHOICES)

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"

    def __str__(self):
        return self.nome