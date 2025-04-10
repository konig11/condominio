from django.db import models
from moradores.models import Morador  # Importa o modelo de Morador

class CategoriaPagamento(models.TextChoices):
    FUNCIONARIO = "Funcionário", "Pagamento de Funcionário"
    SERVICOS = "Serviços", "Pagamento de Serviços"
    ENERGIA = "Energia", "Despesas de Energia"
    AGUA = "Água", "Despesas de Água"
    OUTRO = "Outro", "Outro"
    TAXA='Pagamento de taxa','Pagamento de taxa'

class Pagamento(models.Model):
    morador = models.ForeignKey(Morador, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()
    categoria = models.CharField(max_length=20, choices=CategoriaPagamento.choices, default=CategoriaPagamento.OUTRO)
    descricao = models.TextField(blank=True, null=True)
    is_despesa_condominio = models.BooleanField(default=False)  # Marcar se é uma despesa do condomínio

    def __str__(self):
        tipo_pagamento = "Despesa do Condomínio" if self.is_despesa_condominio else f"Morador: {self.morador}"
        return f"{tipo_pagamento} - {self.valor} MZN ({self.get_categoria_display()})"

