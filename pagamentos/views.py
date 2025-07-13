import json
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Pagamento
from .forms import PagamentoForm
from django.db.models import Sum

# def saldo_condominio(request):
#     total_recebimentos = Pagamento.objects.filter(is_despesa_condominio=False).aggregate(Sum("valor"))["valor__sum"] or 0
#     total_despesas = Pagamento.objects.filter(is_despesa_condominio=True).aggregate(Sum("valor"))["valor__sum"] or 0
#     saldo = total_recebimentos - total_despesas

#     return render(request, "saldo.html", {"saldo": saldo, "recebimentos": total_recebimentos, "despesas": total_despesas})




def saldo_condominio(request):
    recebimentos = Pagamento.objects.filter(is_despesa_condominio=False).aggregate(Sum("valor"))["valor__sum"] or Decimal(0)
    despesas = Pagamento.objects.filter(is_despesa_condominio=True).aggregate(Sum("valor"))["valor__sum"] or Decimal(0)

    if request.user.is_staff:
        template_name = "base_admin.html"
    else:
        template_name = "base_morador.html"
    # Coletar dados para gráfico de pizza
  # Filtra as categorias únicas onde is_despesa_condominio = 0
    categorias = list(
        Pagamento.objects.filter(is_despesa_condominio=1)
        .values_list('categoria', flat=True)
        .distinct()
        )

# Soma os valores por categoria com o mesmo filtro
    valores = [
        Pagamento.objects.filter(is_despesa_condominio=1, categoria=cat)
        .aggregate(Sum("valor"))["valor__sum"] or Decimal(0)
        for cat in categorias
         ]

    # Transformar listas em JSON para usar no template, convertendo Decimal para float
    categorias_json = json.dumps(categorias)
    valores_json = json.dumps([float(v) for v in valores])

    print("Recebimentos:", recebimentos)
    print("Despesas:", despesas)
    print("Categorias JSON:", categorias_json)
    print("Valores JSON:", valores_json)

    context = {
        "recebimentos": float(recebimentos),
        "despesas": float(despesas),
        "saldo": float(recebimentos - despesas),
        "categorias_json": categorias_json,
        "valores_json": valores_json,
        "template_name": template_name
    }

    return render(request, "saldo.html", context)



# def adicionar_pagamento(request):
#     if request.method == "POST":
#         form = PagamentoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Pagamento registrado com sucesso!")
#             return redirect("listar_pagamentos")
#         else:
#             messages.error(request, "Erro ao registrar pagamento. Verifique os dados.")
#     else:
#         form = PagamentoForm()

#     return render(request, "adicionar_pagamento.html", {"form": form})
def adicionar_pagamento(request):
    if request.method == "POST":
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)

            # Se for uma despesa do condomínio, removemos o morador
            if pagamento.is_despesa_condominio:
                pagamento.morador = None  

            pagamento.save()
            messages.success(request, "Pagamento registrado com sucesso!")
            return redirect('listar_pagamentos')
        else:
            messages.error(request, "Erro ao registrar pagamento. Verifique os dados.")
    else:
        form = PagamentoForm()

    return render(request, 'adicionar_pagamento.html', {'form': form})
def listar_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(request, 'listar_pagamentos.html', {'pagamentos': pagamentos})
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)

    if request.method == "POST":
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            return redirect('listar_pagamentos')  # Voltar para a lista após salvar
    else:
        form = PagamentoForm(instance=pagamento)

    return render(request, 'editar_pagamento.html', {'form': form, 'pagamento': pagamento})
def deletar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)

    if request.method == "POST":
        pagamento.delete()
        return redirect('listar_pagamentos')  # Redireciona após excluir

    return render(request, 'deletar_pagamento.html', {'pagamento': pagamento})