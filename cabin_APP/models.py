from django.db import models
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Proyecto(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Eliminado', 'Eliminado'),
    )
    nombre = models.CharField(max_length=60)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    superficie = models.CharField(max_length=200, blank=True, null=True)
    costo_inicial = models.CharField(max_length=200, blank=True, null=True)
    costo_termino = models.CharField(max_length=200, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_termino = models.DateField(blank=True, null=True)
    observacion = models.CharField(max_length=600, blank=True, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre


class Maestro(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Eliminado', 'Eliminado'),
    )
    nombre = models.CharField(max_length=60, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    trabajo = models.CharField(max_length=200, null=True, blank=True)
    contacto = models.PositiveIntegerField(null=True)
    cobro_maestro = models.PositiveIntegerField(null=True, blank=True)
    saldo_inicial = models.PositiveIntegerField(null=True, blank=True)
    saldo_a_deber = models.PositiveIntegerField(null=True, blank=True)
    observacion = models.CharField(max_length=600, null=False, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Eliminado', 'Eliminado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    numero_factura = models.CharField(max_length=50, null=True, blank=True)
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    codigo = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=50, null=True, blank=True)
    proveedor = models.CharField(max_length=60, null=True, blank=True)
    cliente = models.CharField(max_length=60, null=True, blank=True)
    nombre_vendedor = models.CharField(max_length=60, null=True, blank=True)
    observacion = models.CharField(max_length=600, null=True, blank=True)
    subtotal = models.PositiveIntegerField(null=True, blank=True)
    iva = models.CharField(max_length=15, null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=60, null=True, blank=True)
    banco = models.CharField(max_length=60, null=True, blank=True)
    iban = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(null=True, max_length=200, blank=True)
    numero_contacto = models.CharField(max_length=60,null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return str(self.numero_factura)


class Boleta(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Eliminado', 'Eliminado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    numero_boleta = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=50, null=True, blank=True)
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    tipo_boleta = models.CharField(max_length=50, null=True, blank=True)
    hora = models.CharField(max_length=10, null=True, blank=True)
    terminal = models.CharField(max_length=60, null=True, blank=True)
    proveedor = models.CharField(max_length=60, null=True, blank=True)
    rut_empresa = models.CharField(max_length=60, null=True, blank=True)
    rut_cliente = models.CharField(max_length=60, null=True, blank=True)
    cliente = models.CharField(max_length=60, null=True, blank=True)
    nombre_vendedor = models.CharField(max_length=60, null=True, blank=True)
    observacion = models.CharField(max_length=600, null=True, blank=True)
    monto_neto = models.PositiveIntegerField(null=True, blank=True)
    iva = models.CharField(max_length=15, null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    codigo_klap = models.CharField(max_length=60, null=True, blank=True)
    codigo_autorizacion = models.CharField(max_length=60, null=True, blank=True)
    codigo_operacion = models.CharField(max_length=60, null=True, blank=True)
    metodo_pago = models.CharField(max_length=60, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.numero_boleta)

class Materiales(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Eliminado', 'Eliminado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    nombre = models.CharField(max_length=60, null=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    cantidad_disponible = models.PositiveIntegerField(null=True, blank=True)
    precio = models.PositiveBigIntegerField(null=True, blank=True)
    lugar_de_compra = models.CharField(max_length=100,null=True, blank=True)
    fecha_compra = models.DateField(null=True, blank=True)
    observacion = models.CharField(max_length=600, null=True, blank=True)
    facturas = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    boletas = models.ForeignKey(Boleta, on_delete=models.CASCADE, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre

class AsociarMaterial(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Eliminado', 'Eliminado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    material = models.ForeignKey(Materiales, on_delete=models.CASCADE, null=True, blank=True)
    nombre_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.material:
            return self.material.nombre  # Devuelve el nombre del material como cadena
        return "Asociación sin material"
    
    def delete(self, *args, **kwargs):
        # Registrar la asociación en el historial antes de eliminarla
        historial = HistorialAsociacionMateriales.objects.create(
            material=self.material,
            proyecto=self.nombre_proyecto,
            cantidad_asociada=self.cantidad,
            administrador=self.username
        )

        # Restaurar la cantidad_disponible al eliminar la asociación
        self.material.cantidad_disponible += self.cantidad
        self.material.save()

        # Eliminar la asociación
        super().delete(*args, **kwargs)


class AsociarFactura(models.Model):
    nombre_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    numero_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre_proyecto
    
    def delete(self, *args, **kwargs):
        # Eliminar la asociación
        super().delete(*args, **kwargs)

class AsociarBoleta(models.Model):
    nombre_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    numero_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre_proyecto
    
    def delete(self, *args, **kwargs):
        # Eliminar la asociación
        super().delete(*args, **kwargs)

class AsociarMaestro(models.Model):
    nombre_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    nombre_maestro = models.ForeignKey(Maestro, on_delete=models.CASCADE, null=True, blank=True)
    cobro_maestro = models.PositiveIntegerField(null=True, blank=True)
    saldo_inicial = models.PositiveIntegerField(null=True, blank=True)
    saldo_a_deber = models.PositiveIntegerField(null=True, blank=True)
    observacion = models.CharField(max_length=600,null=True, blank=True)
    trabajo = models.CharField(max_length=600,null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre_proyecto
    
    def delete(self, *args, **kwargs):
        # Registrar la asociación en el historial antes de eliminarla
        HistorialAsociacionMaestro.objects.create(
            maestro=self.nombre_maestro,
            proyecto=self.nombre_proyecto,
            administrador=self.username
        )

        # Eliminar la asociación
        super().delete(*args, **kwargs)

class HistorialAsociacionMateriales(models.Model):
    material = models.ForeignKey(Materiales, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    cantidad_asociada = models.PositiveIntegerField()
    fecha_asociacion = models.DateTimeField(auto_now_add=True)
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Asociación #{self.id} - {self.material.observacion} ({self.material.lugar_de_compra})"
    
class HistorialAsociacionMaestro(models.Model):
    maestro = models.ForeignKey(Maestro, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_asociacion = models.DateTimeField(auto_now_add=True)
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Asociación de {self.maestro.nombre} con {self.proyecto.nombre}"


#####Historial de usuario####################    

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(max_length=100)
    details = models.TextField()
    

class PlanUsuario(models.Model):
    ESTADO_CHOICES = (
        ('Mensual', 'Mensual'),
        ('3 Meses', '3 Meses'),
        ('Anual', 'Anual'),
        ('5 años', '5 años'),
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    plan_usuario = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Mensual')
    fecha_registro = models.DateTimeField(null=True)

    def __str__(self):
        return self.usuario.username
    


## errores comunes:
    ###### todo elemento nuevo en la base de datos debe estar en el forms.py y en el html de registro y actualizar aunque no se muestren
    ####### siempre despues de hacer un cambio en la base de datos hacer el makemigrations completo
    ######## revisar bien la base de datos por si no funciona el formulario, puse PositiveIntegerField(numero positivo) y era charfield(texto)
    ####### revisar que sea username, puse usuario XD 
    ####### siempre poner {{form.username}} en el registro.html aunque este no se muestre como tal
    ### si hay error en los forms, no cargan correctamente y solo aparece el placeholder o label es probable que haya error en el views.py por estar llamando a otra base de datos
    
## por hacer: 
## al actualizar el material asociado si pones la misma cantidad del material te dara un numero negativo en cantidad disponible, arreglarlo.
