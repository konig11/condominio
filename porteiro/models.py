from django.db import models
from moradores.models import Morador
from django.contrib.auth.models import User

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
    
class EntradaSaida(models.Model):
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    entrada = models.DateTimeField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.visita.nome_visitante} ({self.visita.morador})"
