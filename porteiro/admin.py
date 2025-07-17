from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from moradores.admin_views import is_admin
from porteiro.forms import PorteiroForm
from porteiro.models import EntradaSaida, Visita
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(is_admin)
def menu_porteiro(request):
    return render(request, 'admin/menu_porteiro.html')
@login_required
@user_passes_test(is_admin)
def historico_entradas_saidas(request):
    registros = EntradaSaida.objects.select_related('visita', 'registrado_por').order_by('-entrada')
    return render(request, 'admin/historico_entradas.html', {'registros': registros})
@login_required
@user_passes_test(is_admin)
def todas_visitas(request):
    visitas = Visita.objects.all().order_by('-data_agendada')
    return render(request, 'admin/todas_visitas.html', {'visitas': visitas})


@login_required
@user_passes_test(is_admin)
def listar_visitas(request):
    visitas = Visita.objects.all().order_by('-data_agendada')

    data = request.GET.get('data')
    morador = request.GET.get('morador')
    status = request.GET.get('status')

    if data:
        visitas = visitas.filter(data_agendada__date=parse_date(data))
    if morador:
        visitas = visitas.filter(morador__nome__icontains=morador)
    if status == 'pendente':
        visitas = visitas.filter(entrada_registrada__isnull=True)
    elif status == 'concluida':
        visitas = visitas.filter(saida_registrada__isnull=False)

    return render(request, 'admin/listar_visitas.html', {'visitas': visitas})

@login_required
@user_passes_test(is_admin)
def criar_porteiro(request):
    if request.method == 'POST':
        form = PorteiroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Porteiro criado com sucesso!")
            return redirect('listar_porteiros')
    else:
        form = PorteiroForm()
    return render(request, 'admin/criar_porteiro.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def listar_porteiros(request):
    porteiro_group = Group.objects.get(name='Porteiro')
    porteiros = User.objects.filter(groups=porteiro_group)
    return render(request, 'admin/listar_porteiros.html', {'porteiros': porteiros})