from django.urls import path
from . import views

urlpatterns = [
    path('visitas/', views.lista_visitas, name='lista_visitas'),
    path('visita/<int:visita_id>/entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('visita/<int:visita_id>/saida/', views.registrar_saida, name='registrar_saida'),
]
