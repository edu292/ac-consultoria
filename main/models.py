from django.db import models

class Prisoes(models.Model):
    nome = models.CharField(max_length=100)
    numero_documento =  models.CharField(max_length=100, null=True)
    numero_bo = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100)
    placa = models.CharField(max_length=100, null=True)
    delito = models.CharField(max_length=100)
    data = models.DateField()
    estrutura_criminal = models.CharField(max_length=100)

    def __str__(self):
        return self.nome