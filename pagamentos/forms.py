from django import forms
from .models import Pagamento

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['morador', 'valor', 'data_pagamento', 'categoria', 'descricao', 'is_despesa_condominio']

        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
