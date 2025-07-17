from django import forms
from pagamentos.models import Pagamento
from porteiro.models import Visita
from .models import Morador, Mensagem
from django.contrib.auth.models import User

class MoradorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar Senha")

    class Meta:
        model = Morador
        fields = ["nome", "telefone", "nr_casa", "nr_moradores", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        telefone = cleaned_data.get("telefone")
        nr_casa = cleaned_data.get("nr_casa")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # 🚨 Verifica se já existe um morador com os mesmos dados
        if Morador.objects.filter(nome=nome).exists():
            self.add_error("nome", "Já existe um morador com este nome.")

        if Morador.objects.filter(telefone=telefone).exists():
            self.add_error("telefone", "Este telefone já está cadastrado.")

        if nr_casa>94:
            self.add_error("Excedeu o numero de casas")
        if Morador.objects.filter(nr_casa=nr_casa).exists():
            self.add_error("nr_casa", "Já existe um morador nesta casa.")

        if len(password)<8:
            self.add_error("password", "A Password Deve ter no minimo 8 caracteres.")
            
        # 🚨 Valida a senha (confirmar senha)
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "As senhas não coincidem.")

        return cleaned_data

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['morador', 'valor', 'data_pagamento', 'categoria', 'descricao', 'is_despesa_condominio']

        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class MensagemForm(forms.ModelForm):
    enviar_para_todos = forms.BooleanField(required=False, label="Enviar para todos os moradores")

    class Meta:
        model = Mensagem
        fields = ['destinatario', 'assunto', 'corpo', 'enviar_para_todos']

    def save(self, remetente=None, commit=True):
        mensagem = super().save(commit=False)
        if not remetente:
            raise ValueError("O remetente deve ser informado.")
        mensagem.remetente = remetente

        if self.cleaned_data['enviar_para_todos']:
            mensagem.destinatario = None  # mensagem para todos

        if commit:
            mensagem.save()
        return mensagem
class AgendarVisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nome_visitante', 'documento', 'data_agendada', 'observacoes']
        widgets = {
            'data_agendada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }