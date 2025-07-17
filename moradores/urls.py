from django.urls import path
from . import views
from . import admin_views 
urlpatterns = [
    path("", views.morador_list, name="morador_list"),
    path("create/", views.morador_create, name="morador_create"),
    path("edit/<int:id>/", views.morador_edit, name="morador_edit"),
    path("delete/<int:id>/", views.morador_delete, name="morador_delete"),
    path('menu/', views.menu_morador, name='menu_morado'),
    path('morador/financeiro/', views.situacao_financeira, name='situacao_financeira'),
    path('mensagens/apagar/<int:mensagem_id>/', views.apagar_mensagem, name='apagar_mensagem'),
    path('mensagens/contar_nao_lidas/', views.minhas_mensagens, name='minhas_mensagens'),
    path('reservas/', views.menu_reservas, name='menu_reservas'),
    path("reservas/reservar-area/", views.reservar_area, name="reservar_area"),
    path("reservas/minhas-reservas/", views.minhas_reservas, name="minhas_reservas"),
    path('reservas/historico/', views.historico_reservas, name='historico_reservas'),
    path('meu-pagamento/', views.pagamento_morador, name='pagamento_morador'),
    path('agendar-visita/', views.agendar_visita, name='agendar_visita'),
    path('minhas-visitas/', views.listar_visitas_morador, name='listar_visitas_morador'),
    
    
        # Rotas do administrador
    path("admin/menu/", admin_views.menu_admin, name="menu_admin"),
    path("admin/reservas/menu", admin_views.gestao_reservas, name="gestao_reservas"),
    path("admin/reservas/", admin_views.lista_reservas, name="lista_reservas"),
    path("admin/reservas_todas/", admin_views.lista_todas_reservas, name="listar_todas_reservas"),
    path("admin/reservas/aprovar/<int:reserva_id>/", admin_views.aprovar_reserva, name="aprovar_reserva"),
    path("admin/reservas/rejeitar/<int:reserva_id>/", admin_views.rejeitar_reserva, name="rejeitar_reserva"),
    path("admin/moradores/", admin_views.menu_morador, name="menu_morador"),
    path('admin/moradores/listar', admin_views.listar_moradores, name='listar_moradores'),
    path('admin/moradores/mensagens', admin_views.lista_mensagens, name='listar_mensagens'),
    path('admin/moradores/enviar_mensagens', admin_views.enviar_mensagem, name='enviar_mensagem'),
    path('admin/moradores/criar/',admin_views.criar_morador, name='criar_morador'),
    path('admin/moradores/editar/<int:morador_id>/', admin_views.editar_morador, name='editar_morador'),
    path('admin/moradores/excluir/<int:morador_id>/', admin_views.excluir_morador, name='excluir_morador'),

]
