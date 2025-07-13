from django.shortcuts import render, redirect, get_object_or_404
from .models import Morador, MensagemLida
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva, AreaSocial, Mensagem
from django.utils.timezone import now
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Morador  # ou como estiver o nome
from .forms import PagamentoForm
from django.http import HttpResponseForbidden, JsonResponse

@login_required
def pagamento_morador(request):
    try:
        morador = request.user.morador  # ajusta isso conforme sua relação User-Morador
    except Morador.DoesNotExist:
        messages.error(request, "Você não está vinculado a um morador.")
        return redirect('home')  # ou onde preferir

    if request.method == "POST":
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.morador = morador
            pagamento.is_despesa_condominio = False
            pagamento.save()
            messages.success(request, "Pagamento registrado com sucesso!")
            return redirect('pagamento_morador')  # ajusta para a página correta
        else:
            messages.error(request, "Erro ao registrar pagamento. Verifique os dados.")
    else:
        form = PagamentoForm()

    # removemos os campos que não devem aparecer para o morador
    form.fields.pop('morador', None)
    form.fields.pop('is_despesa_condominio', None)

    return render(request, 'pagamento_morador.html', {'form': form})


@login_required
def morador_list(request):
    moradores = Morador.objects.all()
    
    return render(request, "list_morador.html", {"moradores": moradores})

@login_required
def morador_create(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        apartamento = request.POST["apartamento"]
        Morador.objects.create(nome=nome, apartamento=apartamento)
        return redirect("morador_list")
    return render(request, "moradors/morador_form.html")

@login_required
def morador_edit(request, id):
    morador = get_object_or_404(Morador, id=id)
    if request.method == "POST":
        morador.nome = request.POST["nome"]
        morador.apartamento = request.POST["apartamento"]
        morador.save()
        return redirect("morador_list")
    return render(request, "moradors/morador_form.html", {"morador": morador})

@login_required
def morador_delete(request, id):
    morador = get_object_or_404(Morador, id=id)
    morador.delete()
    return redirect("morador_list")


@login_required
def reservar_area(request):
    if request.method == "POST":
        area_id = request.POST["areaSocial"]
        data = request.POST["data"]
        hora_inicio = request.POST["hora_inicio"]
        hora_fim = request.POST["hora_fim"]

        area = AreaSocial.objects.get(id=area_id)

        # Verifica se já existe uma reserva para essa área no mesmo dia e horário
        conflito = Reserva.objects.filter(
            area_social=area,
            data=data,
            hora_inicio__lt=hora_fim, 
            hora_fim__gt=hora_inicio
        ).exists()

        if conflito:
            messages.error(request, "Já existe uma reserva para essa área nesse horário!")
            return redirect("reservar_area")

        # Cria a reserva pendente
        morador = Morador.objects.get(usuario=request.user)
        Reserva.objects.create(
            morador=morador,
            area_social=area,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            status="Pendente"
        )

        messages.success(request, "Reserva enviada para aprovação!")
        return redirect("minhas_reservas")

    areaSocial = AreaSocial.objects.all()
    return render(request, "reservas/reservar_area.html", {"areaSocial": areaSocial})
@login_required
def menu_reservas(request):
    return render(request, 'reservas/menu_reeservas.html')

@login_required
def historico_reservas(request):
    morador = Morador.objects.get(usuario=request.user)
    historico = Reserva.objects.filter(morador=morador, data__lt=now().date()).order_by('-data')
    return render(request, 'reservas/historico_reservas.html', {'historico': historico})

@login_required
def minhas_reservas(request):
    # Primeiro, encontramos o morador correspondente ao usuário logado
    morador = Morador.objects.get(usuario=request.user)
    
    # Agora, filtramos as reservas desse morador
    reservas = Reserva.objects.filter(morador=morador, data__gte=now().date()).order_by('data')

    return render(request, 'reservas/minhas_reservas.html', {'reservas': reservas})


def menu_morador(request):
    return render(request, 'menu_morador.html')

def reservas_morador(request):
    return render(request, 'reservas/menu_reeservas.html')

def situacao_financeira(request):
    return redirect("saldo_condominio")


def minhas_mensagens(request):
    morador = Morador.objects.get(usuario=request.user)
    mensagens = Mensagem.objects.filter(
        Q(destinatario=morador) | Q(destinatario__isnull=True)
    ).order_by('-data_envio')

    # Para cada mensagem geral (destinatario=None) não lida pelo morador, registre a leitura
    for mensagem in mensagens:
        if mensagem.destinatario is None:
            # Mensagem geral
            MensagemLida.objects.get_or_create(morador=morador, mensagem=mensagem)
        else:
            # Mensagem direta
            if not mensagem.lida:
                mensagem.lida = True
                mensagem.save()

    return render(request, 'minhas_mensagens.html', {'mensagens': mensagens})

@login_required
def apagar_mensagem(request, mensagem_id):
    morador = Morador.objects.get(usuario=request.user)
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    
    if mensagem.destinatario != morador:
        return HttpResponseForbidden("Você não tem permissão para apagar esta mensagem.")
    
    mensagem.delete()
    return redirect('minhas_mensagens')

# @login_required
# def contar_mensagens_nao_lidas(request):
#     count = Mensagem.objects.filter(
#         Q(destinatario=request.user) | Q(destinatario__isnull=True),
#         lida=False
#     ).count()
#     return JsonResponse({'nao_lidas': count})