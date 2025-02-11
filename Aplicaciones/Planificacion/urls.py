from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='plantilla-admin'),
    

    # Rutas para Quejas
    path('quejas/', views.listar_quejas, name='listar_quejas'),
    path('quejas/crear/', views.crear_queja, name='crear_queja'),
    path('quejas/detalle/<int:id_queja>/', views.detalle_queja, name='detalle_queja'),

    # Rutas para Viviendas
    path('viviendas/', views.listar_viviendas, name='listar_viviendas'),
    path('viviendas/crear/', views.crear_vivienda, name='crear_vivienda'),
    path('viviendas/detalle/<int:id_vivienda>/', views.detalle_vivienda, name='detalle_vivienda'),
    path('viviendas/editar/<int:id_vivienda>/', views.editar_vivienda, name='editar_vivienda'),
    path('viviendas/eliminar/<int:id_vivienda>/', views.eliminar_vivienda, name='eliminar_vivienda'),

    # Rutas para Constructoras
    path('constructoras/', views.listar_constructoras, name='listar_constructoras'),
    path('constructoras/crear/', views.crear_constructora, name='crear_constructora'),
    path('constructoras/detalle/<int:id_constructora>/', views.detalle_constructora, name='detalle_constructora'),
    path('constructoras/editar/<int:id_constructora>/', views.editar_constructora, name='editar_constructora'),
    path('constructoras/eliminar/<int:id_constructora>/', views.eliminar_constructora, name='eliminar_constructora'),

    # Rutas para Clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/detalle/<int:id_cliente>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/editar/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),


    # Rutas para Actividades
    path('actividades/', views.listar_actividades, name='listar_actividades'),
    path('actividades/crear/', views.crear_actividad, name='crear_actividad'),
    path('actividades/detalle/<int:id_actividad>/', views.detalle_actividad, name='detalle_actividad'),
    path('actividades/editar/<int:id_actividad>/', views.editar_actividad, name='editar_actividad'),
    path('actividades/eliminar/<int:id_actividad>/', views.eliminar_actividad, name='eliminar_actividad'),


] 



