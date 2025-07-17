from django import forms
from .models import Visita
from django.contrib.auth.models import User, Group

class PorteiroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hashear a senha
        if commit:
            user.save()
            porteiro_group, created = Group.objects.get_or_create(name='Porteiro')
            user.groups.add(porteiro_group)
        return user


class VisitaRapidaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nome_visitante', 'morador', 'observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
