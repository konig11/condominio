from django.shortcuts import render, get_object_or_404, redirect
from .models import Visita
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test

def is_porteiro(user):
    return user.groups.filter(name='Porteiros').exists()

@login_required
@user_passes_test(is_porteiro)
def lista_visitas(request):
    visitas = Visita.objects.filter(data_agendada__date=now().date()).order_by('data_agendada')
    return render(request, 'porteiro/lista_visitas.html', {'visitas': visitas})

@login_required
@user_passes_test(is_porteiro)
def registrar_entrada(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    visita.entrada_registrada = now()
    visita.save()
    return redirect('lista_visitas')

@login_required
@user_passes_test(is_porteiro)
def registrar_saida(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    visita.saida_registrada = now()
    visita.save()
    return redirect('lista_visitas')
