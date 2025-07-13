from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Reserva,Mensagem
from django.contrib.auth.models import User
from .models import Morador
from .forms import MoradorForm,MensagemForm  # Vamos criar esse formulário a seguir


@login_required
def menu_admin(request):
    return render(request, "admin/menu_admin.html")

# Função para verificar se o usuário é administrador
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def menu_morador(request):
    return render(request, "admin/menu_morador.html")


@login_required
def gestao_reservas(request):
    return render(request, "admin/menu_reservas.html")


@user_passes_test(is_admin)  # Apenas administradores podem acessar
def lista_todas_reservas(request):
    reservas = Reserva.objects.filter(status="Pendente").order_by("data")
    return render(request, "admin/listar_todas_reservas.html", {"reservas_pendentes": reservas})

@login_required
def saldo_condominio(request):
    return redirect('saldo_condominio')


# Página para listar todas as reservas pendentes
@login_required
@user_passes_test(is_admin)  # Apenas administradores podem acessar
def lista_reservas(request):
    reservas = Reserva.objects.filter(status="Pendente").order_by("data")
    return render(request, "admin/listar_reservas_pendentes.html", {"reservas_pendentes": reservas})

# Aprovar reserva
@login_required
@user_passes_test(is_admin)
def aprovar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.status = "Aprovado"
    reserva.save()

    # Enviar mensagem ao morador
    Mensagem.objects.create(
        remetente=request.user,
        destinatario=reserva.morador,
        assunto="Reserva de área social aprovada",
        corpo=f"Sua reserva para {reserva.area_social} na data {reserva.data} foi aprovada."
    )

    messages.success(request, "Reserva aprovada com sucesso!")
    return redirect("lista_reservas")

@login_required
@user_passes_test(is_admin)
def rejeitar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.status = "Rejeitado"
    reserva.save()

    # Enviar mensagem ao morador
    Mensagem.objects.create(
        remetente=request.user,
        destinatario=reserva.morador,
        assunto="Reserva de área social rejeitada",
        corpo=f"Sua reserva para {reserva.area_social} na data {reserva.data} foi rejeitada."
    )

    messages.error(request, "Reserva rejeitada.")
    return redirect("lista_reservas")


# Lista de moradores
@login_required
@user_passes_test(is_admin)
def listar_moradores(request):
    moradores = Morador.objects.all()
    return render(request, 'admin/listar_moradores.html', {'moradores': moradores})

# Criar morador + usuário automaticamente
@login_required
@user_passes_test(is_admin)
def criar_morador(request):
    if request.method == 'POST':
        form = MoradorForm(request.POST)
        if form.is_valid():
            morador = form.save(commit=False)

            # Criar usuário associado ao morador
            username = request.POST.get('nome').lower()
            password = request.POST.get('password')

            if username and password:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                morador.usuario = user  # Associa o usuário ao morador

            morador.save()
            messages.success(request, "Morador criado com sucesso!")
            return redirect('listar_moradores')
        else:
            messages.error(request, "Erro ao atualizar morador. Verifique os dados.")
    else:
        form = MoradorForm()

    return render(request, 'admin/criar_morador.html', {'form': form})

# Editar morador
@login_required
@user_passes_test(is_admin)
def editar_morador(request, morador_id):
    morador = get_object_or_404(Morador, id=morador_id)
    
    if request.method == 'POST':
        form = MoradorForm(request.POST, instance=morador)
        if form.is_valid():
            form.save()
            messages.success(request, "Morador atualizado com sucesso!")
            return redirect('listar_moradores')
        else:
            messages.error(request, "Erro ao atualizar morador. Verifique os dados.")
    else:
        form = MoradorForm(instance=morador)

    return render(request, 'admin/editar_morador.html', {'form': form, 'morador': morador})

# Excluir morador
@login_required
@user_passes_test(is_admin)
def excluir_morador(request, morador_id):
    morador = get_object_or_404(Morador, id=morador_id)
    morador.delete()
    messages.success(request, "Morador excluído com sucesso!")
    return redirect('listar_moradores')

@login_required
@user_passes_test(is_admin)
def lista_mensagens(request):
    mensagens = Mensagem.objects.all().order_by('-data_envio')
    return render(request, 'admin/listar_mensagens.html', {'mensagens': mensagens})

@login_required
@user_passes_test(is_admin)
def enviar_mensagem(request):
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            form.save(remetente=request.user)  # ✅ passa o usuário
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('listar_mensagens')
    else:
        form = MensagemForm()
    return render(request, 'admin/enviar_mensagem.html', {'form': form})
