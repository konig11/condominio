from .models import Mensagem, Morador, MensagemLida
from django.db.models import Q

def mensagens_nao_lidas(request):
    if request.user.is_authenticated:
        morador = Morador.objects.filter(usuario=request.user).first()
        if morador:
            mensagens_diretas = Mensagem.objects.filter(destinatario=morador, lida=False)
            mensagens_para_todos = Mensagem.objects.filter(destinatario__isnull=True).exclude(
                id__in=MensagemLida.objects.filter(morador=morador).values_list('mensagem_id', flat=True)
            )
            count = mensagens_diretas.count() + mensagens_para_todos.count()
        else:
            count = 0
    else:
        count = 0
    return {'mensagens_nao_lidas': count}
