from django.urls import path
from .views import adicionar_pagamento, deletar_pagamento, editar_pagamento, listar_pagamentos
from .views import saldo_condominio

urlpatterns = [
    path('', listar_pagamentos, name='listar_pagamentos'),
    path("adicionar/", adicionar_pagamento, name="adicionar_pagamento"),
    path("saldo/", saldo_condominio, name="saldo_condominio"),
    path('editar/<int:pagamento_id>/', editar_pagamento, name='editar_pagamento'),
    path('deletar/<int:pagamento_id>/', deletar_pagamento, name='deletar_pagamento'),
]
