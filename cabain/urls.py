"""cabain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from cabin_APP.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # pagina principal del sitio
    path('', index, name='index'),

    # navbar
    path('navbar/', template_navbar, name="navbar"),

    # Inicio de sesion
    path('salir/', salir, name="salir"),
    path('registro/', registrarse, name='registro'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cuenta/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    
    # menu principal
    path('menu_principal/', main_menu, name='menu_principal'),
    path('proyecto_maestro/', menu_proyecto_maestros, name="proyecto/maestro"),
    path('factura_boleta/', menu_factura_boleta, name="boleta/factura"),

    # Proyecto
    path('vista_proyecto/<int:id>', vista_proyecto, name="vista_proyecto"),
    path('registro_proyecto/', registrar_proyecto, name="formulario_proyecto"),
    path('lista_proyectos/', listar_proyecto, name="listar_proyecto" ),
    path('actualizar_proyecto/<int:id>', actualizar_proyecto, name="actualizar_proyecto"),
    path('proyecto_eliminar/<id>/', eliminar_proyecto, name="eliminar_proyecto"),

    # Maestro
    path('registro_maestro/', registrar_maestro, name="registrar_maestro"),
    path('listar_maestro/', listar_maestro, name="listar_maestro"),
    path('maestro_eliminar/<id>/', eliminar_maestro, name="eliminar_maestro"),
    path('actualizar_maestro/<int:id>', actualizar_maestro, name="actualizar_maestro"),

    # Materiales
    path('registro_materiales/', registrar_material, name="registrar_material"),
    path('lista_materiales/', listar_materiales, name="listar_materiales"),
    path('actualizar_material/<int:id>', actualizar_material, name="actualizar_material"),
    path('eliminar_material/<id>/', eliminar_material, name="eliminar_material"),

    # Factura
    path('vista_factura/<int:id>', vista_factura, name="vista_factura"),
    path('registro_factura/', registrar_factura, name="registrar_factura"),
    path('listado_factura/', listar_factura, name="listar_factura"),
    path('actualizar_factura/<int:id>', actualizar_factura, name="actualizar_factura"),
    path('eliminar_factura/<id>/', eliminar_factura, name="eliminar_factura"),

    # Boleta
    path('vista_boleta/<int:id>', vista_boleta, name="vista_boleta"),
    path('registro_boleta/', registrar_boleta, name="registrar_boleta"),
    path('listado_boleta/', listar_boleta, name="listar_boleta"),
    path('actualizar_boleta/<int:id>', actualizar_boleta, name="actualizar_boleta"),
    path('eliminar_boleta/<id>/', eliminar_boleta, name="eliminar_boleta"),
    
    #Asociaciones
    path('actualizar_material_asociado/<int:id>/', actualizar_material_asociado, name='actualizar_material_asociado'),
    path('actualizar_maestro_asociado/<int:id>/', actualizar_maestro_asociado, name='actualizar_maestro_asociado'),
    path('eliminar_material_asociado/<id>/', eliminar_material_asociado, name="eliminar_material_asociado"),
    path('eliminar_factura_asociada/<id>/', eliminar_factura_asociada, name="eliminar_factura_asociada"),
    path('eliminar_boleta_asociada/<id>/', eliminar_boleta_asociada, name="eliminar_boleta_asociada"),
    path('eliminar_maestro_asociado/<id>/', eliminar_maestro_asociado, name="eliminar_maestro_asociado"),

    # reseteo de contraseña (olvide mi contraseña)
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # cambiar contraseña
    path('cambiar_contraseña/', change_password, name='cambiar_contrasenea'),

    # cambiar nombre usuario
    path('cambiar_nombre/', cambiar_nombre_usuario, name='cambiar_nombre'),

    # cambiar email
    path('cambiar_email/', cambiar_email, name='cambiar_email'),

    # historial usuario
    path('historial_usuario/', historial_actividad, name='historial_usuario'),

    #contacto
    path('contactanos/', contacto, name='contacto'),

    #precios
    path('planes_precios/', planes_precios, name='planes_precios'),

    # Error
    path('error/', error, name="error")
]
