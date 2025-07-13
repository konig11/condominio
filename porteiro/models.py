from django.db import models
from moradores.models import Morador

class Visita(models.Model):
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    nome_visitante = models.CharField(max_length=100)
    documento = models.CharField(max_length=50, blank=True, null=True)
    data_agendada = models.DateTimeField()
    observacoes = models.TextField(blank=True)
    entrada_registrada = models.DateTimeField(blank=True, null=True)
    saida_registrada = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome_visitante} - {self.morador}"
