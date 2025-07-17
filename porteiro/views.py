from django.utils import timezone  # ✅ Correto para Django
from datetime import date
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Visita
from .models import EntradaSaida
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Visita, EntradaSaida
from .forms import VisitaRapidaForm

def is_porteiro(user):
    return user.groups.filter(name='Porteiro').exists()


@login_required
@user_passes_test(is_porteiro)
def lista_visitas(request):
    hoje = date.today()
    visitas = Visita.objects.filter(
        data_agendada__date=hoje
    ).order_by('data_agendada')
    return render(request, 'lista_visitas.html', {'visitas': visitas})
@login_required
@user_passes_test(is_porteiro)
def menu_porteiro(request):
    return render(request,'menu_porteiro.html')
@login_required
@user_passes_test(is_porteiro)
def registrar_entrada(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    visita.entrada_registrada = timezone.now()
    visita.save()
    EntradaSaida.objects.create(visita=visita, entrada=timezone.now(), registrado_por=request.user)
    return redirect('lista_visitas')

@login_required
@user_passes_test(is_porteiro)
def registrar_saida(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    visita.saida_registrada = timezone.now()
    visita.save()
    registro = EntradaSaida.objects.filter(visita=visita).last()
    if registro and not registro.saida:
        registro.saida = timezone.now()
        registro.save()
    return redirect('lista_visitas')

@login_required
@user_passes_test(is_porteiro)
def registrar_visita_na_hora(request):
    if request.method == 'POST':
        form = VisitaRapidaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.data_agendada = timezone.now()
            visita.entrada_registrada = timezone.now()
            visita.save()
            EntradaSaida.objects.create(visita=visita, entrada=timezone.now(), registrado_por=request.user)
            messages.success(request, "Visita registrada com sucesso.")
            return redirect('lista_visitas')
    else:
        form = VisitaRapidaForm()
    
    return render(request, 'registrar_visita_na_hora.html', {'form': form})