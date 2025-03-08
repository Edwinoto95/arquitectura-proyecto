from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Cambiamos la ruta principal a login
    path('logout/', views.logout, name='logout'),
    path('inicio/', views.inicio, name='inicio'),
    
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/form/', views.cliente_form, name='cliente_form'),
    path('clientes/form/<int:id>/', views.cliente_form, name='cliente_update'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    path('proyectos/', views.ProyectoListView.as_view(), name='proyecto_list'),
    path('proyectos/<int:pk>/', views.ProyectoDetailView.as_view(), name='proyecto_detail'),
    path('proyectos/nuevo/', views.ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyectos/<int:pk>/editar/', views.ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyectos/<int:pk>/eliminar/', views.ProyectoDeleteView.as_view(), name='proyecto_delete'),
]