from django.urls import path
from . import views
from . import admin

urlpatterns = [
    path('visitas/', views.lista_visitas, name='lista_visitas'),
    path('visita/<int:visita_id>/entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('visita/<int:visita_id>/saida/', views.registrar_saida, name='registrar_saida'),
    path('porteiro/', views.menu_porteiro, name='menu_porteiro'),
    path('registrar-visita-na-hora/', views.registrar_visita_na_hora, name='registrar_visita_na_hora'),
    path('admin/porteiros/', admin.menu_porteiro, name='menu_porteiro_admin'),
    path('admin/porteiros/criar/', admin.criar_porteiro, name='criar_porteiro'),
    path('admin/porteiros/', admin.listar_porteiros, name='listar_porteiros'),
    path('admin/porteiros/historico_entraga',admin.historico_entradas_saidas,name='historico_entradas_saidas'),
    path('admin/porteiros/todas_visitas',admin.todas_visitas,name='todas_visitas'),
    path('admin/porteiros/listar_porteiros',admin.listar_porteiros,name='listar_porteiros')
]
