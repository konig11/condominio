from django.contrib.auth.models import User


from django.utils import timezone

from django.db import models

class Morador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=40, null=True, blank=True)
    nr_casa = models.CharField(max_length=40, null=True, blank=True)
    nr_moradores = models.IntegerField(null=True, blank=True)

    

    def __str__(self):
        return f"{self.nome} - Casa {self.nr_casa}"

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(Morador, on_delete=models.CASCADE, related_name='mensagens_recebidas', null=True, blank=True)
    assunto = models.CharField(max_length=255)
    corpo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.assunto} - de {self.remetente.username} para {self.destinatario.username}"
    
class AreaSocial(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Reserva(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aprovada', 'Aprovada'),
        ('Rejeitada', 'Rejeitada'),
    ]

    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    area_social = models.ForeignKey(AreaSocial, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')

    def __str__(self):
        return f"{self.area_social} - {self.data} ({self.hora_inicio} - {self.hora_fim})"

class MensagemLida(models.Model):
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE)
    data_leitura = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('morador', 'mensagem')  # Garante que só exista 1 leitura por morador/mensagem
