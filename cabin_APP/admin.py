from django.contrib import admin
from . import models as m
from .models import *   
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class PlanUsuarioInline(admin.StackedInline):
    model = PlanUsuario
    can_delete = False
    verbose_name_plural = 'Plan Usuario'

class UserAdmin(UserAdmin):
    inlines = (PlanUsuarioInline,)

# Desregistrar el modelo User original y registrar el nuevo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class HistorialAsociacionAdmin(admin.ModelAdmin):
    list_display = ('material', 'proyecto', 'cantidad_asociada', 'fecha_asociacion', 'administrador', 'material_observacion', 'material_lugar_compra')
    search_fields = ('material__nombre', 'proyecto__nombre', 'administrador__username', 'administrador__id', 'administrador__first_name', 'administrador__last_name')

    def material_observacion(self, obj):
        return obj.material.observacion
    material_observacion.short_description = 'Observación'

    def material_lugar_compra(self, obj):
        return obj.material.lugar_de_compra
    material_lugar_compra.short_description = 'Proveedor'

# Registra el modelo personalizado en el panel de administración
admin.site.register(HistorialAsociacionMateriales, HistorialAsociacionAdmin)


class HistorialAsociacionMaestroAdmin(admin.ModelAdmin):
    list_display = ('maestro', 'proyecto', 'fecha_asociacion', 'administrador', 'administrador_id')
    search_fields = ('maestro__nombre', 'proyecto__nombre', 'administrador__username', 'administrador__id', 'administrador__first_name', 'administrador__last_name')

admin.site.register(HistorialAsociacionMaestro, HistorialAsociacionMaestroAdmin)


class MaestroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'username_id', 'trabajo', 'contacto', 'cobro_maestro', 'saldo_inicial', 'saldo_a_deber', 'observacion')
    list_filter = ('estado',) 
    search_fields = ('nombre', 'id', 'trabajo', 'username__username') 

admin.site.register(Maestro, MaestroAdmin)

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado','username', 'superficie', 'costo_inicial', 'costo_termino', 'fecha_inicio', 'fecha_termino', 'observacion')
    list_filter = ('estado',) 
    search_fields = ('nombre', 'superficie', 'costo_inicial', 'costo_termino', 'fecha_inicio', 'fecha_termino', 'observacion', 'username__username')  # Agrega todos los campos que deseas buscar

admin.site.register(Proyecto, ProyectoAdmin)

class materialesAsociadoUsuario(admin.ModelAdmin):
    list_display = ('username_id', 'username', 'material', 'nombre_proyecto', 'cantidad', 'get_observacion', 'get_proveedor', 'estado')
    list_filter = ('estado',) 
    search_fields = ('username__username', 'username__id', 'material__nombre', 'nombre_proyecto__nombre', 'cantidad', 'material__observacion', 'material__lugar_de_compra')

    def get_observacion(self, obj):
        if obj.material:
            return obj.material.observacion
        return None
    get_observacion.short_description = 'Observación'

    def get_proveedor(self, obj):
        if obj.material:
            return obj.material.lugar_de_compra
        return None
    get_proveedor.short_description = 'Proveedor'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Actualiza el estado de las asociaciones cuando el estado del material cambia a 'Eliminado'
        if obj.material.estado == 'Eliminado':
            AsociarMaterial.objects.filter(material=obj.material).update(estado='Eliminado')

admin.site.register(AsociarMaterial, materialesAsociadoUsuario)

class MaterialesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'username', 'cantidad', 'cantidad_disponible', 'precio', 'lugar_de_compra', 'fecha_compra', 'observacion')
    list_filter = ('estado',)
    search_fields = ('nombre', 'lugar_de_compra', 'username__username')

admin.site.register(Materiales, MaterialesAdmin)

class BoletaAdmin(admin.ModelAdmin):
    list_display = ('numero_boleta', 'estado', 'username', 'fecha_emision', 'fecha_vencimiento', 'tipo_boleta', 'proveedor', 'cliente')
    list_filter = ('estado', 'tipo_boleta')
    search_fields = ('numero_boleta', 'proveedor', 'cliente', 'rut_empresa', 'rut_cliente', 'nombre_vendedor', 'username__username')

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'estado', 'username', 'fecha_emision', 'fecha_vencimiento', 'proveedor', 'cliente')
    list_filter = ('estado',)
    search_fields = ('numero_factura', 'proveedor', 'cliente', 'nombre_vendedor', 'username__username')

# Registra los modelos personalizados en el panel de administración
admin.site.register(Boleta, BoletaAdmin)
admin.site.register(Factura, FacturaAdmin)

class HistorialUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user','user_id', 'timestamp', 'activity_type', 'details')
    search_fields = ('user__username', 'user__id', 'timestamp', 'activity_type', 'details')

admin.site.register(ActivityLog, HistorialUsuarioAdmin)











