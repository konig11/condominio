from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Importa o modelo padrão do Django
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

def user_list(request):
    users = User.objects.all()  # Agora busca os usuários do modelo padrão
    return render(request, 'usuario/user_list.html', {'users': users})

def register_user(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            username = request.POST['usuario']  # Django usa "username"
            senha = request.POST['senha']

            # Criando um novo usuário com o modelo padrão
            user = User.objects.create_user(username=username, password=senha)
            user.first_name = nome  # Armazena o nome no campo padrão 'first_name'
            user.save()

            return redirect('user_list')
        except Exception as e:
            return HttpResponse(f"Erro: {e}")  # Mostra erros no navegador

    return render(request, 'usuario/register_user.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("usuario").lower()
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirecionamento baseado no tipo de usuário
            if user.is_staff:
                return redirect("menu_admin")
            elif user.groups.filter(name="Porteiro").exists():
                return redirect("menu_porteiro")
            else:
                return redirect("menu_morado")

        else:
            messages.error(request, "O nome de usuário e/ou a senha estão incorretos")

    return render(request, "usuario/login_user.html")


def logout_view(request):
    logout(request)
    list(messages.get_messages(request)) 
    return redirect("login")  # Redireciona para a página de login
