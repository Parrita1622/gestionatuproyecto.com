from django import forms
from .models import *
from django.contrib.auth.models import User

class FormUser(forms.ModelForm):
    #contrasena2 = forms.CharField(max_length=100)
    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre usuario"}),
            'first_name': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre"}),
            'last_name': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"apellido"}),
            'email': forms.EmailInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"email"}),
            'password': forms.PasswordInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"contraseña"})
        }
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo',
            'password': 'Contraseña',
                       
        }
        fields = ['username', 'first_name', 'last_name',  'email', 'password',]

###############PROYECTO######################################

class FormCreateProject(forms.ModelForm):
    class Meta:
        model = Proyecto
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre proyecto"}),
            'superficie': forms.TextInput(attrs={"type":"number","class":"form-control", "id":"floatingInput", "placeholder":"superficie(M2)"}),
            'costo_inicial': forms.TextInput(attrs={"type":"text","class":"form-control", "id":"floatingInput", "placeholder":"costo inicial", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'fecha_inicio': forms.DateInput(attrs={"type":"date","class":"form-control", "id":"floatingInput", "placeholder":"fecha de inicio"}),
            'fecha_termino': forms.DateInput(attrs={"type":"date","class":"form-control", "id":"floatingInput", "placeholder":"fecha de termino"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"observación", "maxlength": "600"})
        }
        fields = '__all__'

class FormActualizarProyecto(forms.ModelForm):
    
    class Meta:
        model = Proyecto
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre proyecto"}),
            'superficie': forms.TextInput(attrs={"type":"text","class":"form-control", "id":"floatingInput", "placeholder":"superficie(M2)"}),
            'costo_inicial': forms.TextInput(attrs={"type":"text","class":"form-control", "id":"floatingInput", "placeholder":"costo inicial", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'fecha_inicio': forms.DateInput(attrs={"type":"date","class":"form-control", "id":"floatingInput", "placeholder":"fecha inicial"}),
            'fecha_termino': forms.DateInput(attrs={"type":"date","class":"form-control", "id":"floatingInput", "placeholder":"fecha termino"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"observacion", "maxlength": "600"})
        }
        fields = '__all__'

#################MAESTRO#######################

class FormRegistrarMaestro(forms.ModelForm):
    class Meta:
        model = Maestro
        widgets = {
            'estado':forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre maestro"}),
            'trabajo': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"trabajo maestro"}),
            'contacto': forms.TextInput(attrs={"type":"number", "class":"form-control", "id":"floatingInput", "placeholder":"contacto"}),
            'cobro_maestro': forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"cobro maestro", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'saldo_inicial': forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"saldo", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'saldo_a_deber': forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"saldo a deber", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"observacion", "maxlength": "600"})
        }
        fields = '__all__'


class FormActualizarMaestro(forms.ModelForm):
    class Meta:
        model = Maestro
        widgets = {
            'estado':forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre maestro"}),
            'trabajo': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"trabajo maestro"}),
            'contacto': forms.TextInput(attrs={"type":"number", "class":"form-control", "id":"floatingInput", "placeholder":"contacto"}),
            'cobro_maestro': forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"cobro maestro", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'saldo_inicial': forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"saldo", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'saldo_a_deber': forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"saldo a deber", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"observacion", "maxlength": "600"})
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FormActualizarMaestro, self).__init__(*args, **kwargs)

#####################MATERIAL############################

class FormRegistrarMaterial(forms.ModelForm):
    class Meta:
        model = Materiales
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'cantidad_disponible': forms.HiddenInput,
            'total': forms.HiddenInput,
            'facturas': forms.Select(attrs={"class":"form-select"}),
            'boletas': forms.Select(attrs={"class":"form-select"}),
            'nombre': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre"}),
            'cantidad': forms.TextInput(attrs={"type":"text","class":"form-control", "id":"floatingInput", "placeholder":"cantidad", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $, 0 y letras"}),
            'precio': forms.NumberInput(attrs={"type":"text","class":"form-control", "id":"floatingInput", "placeholder":"precio","required":"true", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'fecha_compra':forms.DateInput(attrs={"type":"date","class":"form-control", "id":"floatingInput", "placeholder":"fecha de compra"}),
            'lugar_de_compra': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"proveedor"}),
            'observacion': forms.Textarea(attrs={"type": "text","class": "form-control", "id": "floatingInput", "placeholder": "observacion"})

        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(FormRegistrarMaterial, self).__init__(*args, **kwargs)
            if user:
                self.fields['facturas'].queryset = Factura.objects.filter(username=user)
                self.fields['boletas'].queryset = Factura.objects.filter(username=user)

    
class FormActualizarMaterial(forms.ModelForm):
    class Meta:
        model = Materiales
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'cantidad_disponible': forms.HiddenInput,
            'total': forms.HiddenInput,
            'facturas': forms.Select(attrs={"class":"form-select"}),
            'boletas': forms.Select(attrs={"class":"form-select"}),
            'nombre': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"nombre"}),
            'cantidad': forms.TextInput(attrs={"type":"text","class":"form-control", "id":"floatingInput", "placeholder":"cantidad", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'precio': forms.TextInput(attrs={"type":"text","class":"form-control", "id":"floatingInput", "placeholder":"precio", "required":"true", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'lugar_de_compra': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"proveedor"}),
            'fecha_compra':forms.DateInput(attrs={"type":"date","class":"form-control", "id":"floatingInput", "placeholder":"fecha de compra"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"observacion", "maxlength": "600"})
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(FormActualizarMaterial, self).__init__(*args, **kwargs)
            if user:
                self.fields['facturas'].queryset = Factura.objects.filter(username=user)
                self.fields['boletas'].queryset = Factura.objects.filter(username=user)

##########################FACTURA#######################

class FormRegistrarFactura(forms.ModelForm):
    class Meta:
        model = Factura
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre_proyecto': forms.HiddenInput,
            'numero_factura': forms.TextInput(attrs={"class":"form-control", "placeholder":"numero factura", "required":"true"}),
            'fecha_emision': forms.DateInput(attrs={"type":"date","class":"form-control", "required":"true"}),
            'fecha_vencimiento': forms.DateInput(attrs={"type":"date","class":"form-control"}),
            'codigo': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"codigo"}),
            'direccion': forms.TextInput(attrs={"class":"form-control", "placeholder":"direccion", "required":"true"}),
            'proveedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"proveedor", "required":"true"}),
            'cliente': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre cliente"}),
            'nombre_vendedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre vendedor"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "placeholder":"observación", "rows": "3", "maxlength": "600"}),
            'subtotal': forms.TextInput(attrs={"type":"text","class":"form-control", "placeholder":"subtotal", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'iva': forms.TextInput(attrs={"class":"form-control", "placeholder":"iva"}),
            'total': forms.TextInput(attrs={"type":"text","class":"form-control", "placeholder":"total", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'metodo_pago': forms.TextInput(attrs={"class": "form-control", "placeholder": "metodo pago", "required": False}),
            'banco': forms.TextInput(attrs={"class":"form-control", "placeholder":"banco"}),
            'iban': forms.TextInput(attrs={"class":"form-control", "placeholder":"iban"}),
            'email': forms.EmailInput(attrs={"type":"email", "class":"form-control", "placeholder":"email"}),
            'numero_contacto': forms.TextInput(attrs={"type":"text", "class":"form-control", "placeholder":"numero contacto"})
                  
        }
        fields = '__all__'

class FormActualizarFactura(forms.ModelForm):
    class Meta:
        model = Factura
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre_proyecto': forms.HiddenInput,
            'numero_factura': forms.TextInput(attrs={"class":"form-control", "placeholder":"numero factura"}),
            'fecha_emision': forms.DateInput(attrs={"type":"date","class":"form-control", "required":"true"}),
            'fecha_vencimiento': forms.DateInput(attrs={"type":"date","class":"form-control"}),
            'codigo': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"codigo"}),
            'direccion': forms.TextInput(attrs={"class":"form-control", "placeholder":"direccion", "required":"true"}),
            'proveedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"proveedor", "required":"true"}),
            'cliente': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre cliente"}),
            'nombre_vendedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre vendedor"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "placeholder":"observación", "rows": "3", "maxlength": "600"}),
            'subtotal': forms.TextInput(attrs={"type":"text","class":"form-control", "placeholder":"subtotal", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'iva': forms.TextInput(attrs={"class":"form-control", "placeholder":"iva"}),
            'total': forms.TextInput(attrs={"type":"text","class":"form-control", "placeholder":"total", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'metodo_pago': forms.TextInput(attrs={"class":"form-control", "placeholder":"metodo pago"}),
            'banco': forms.TextInput(attrs={"class":"form-control", "placeholder":"banco"}),
            'iban': forms.TextInput(attrs={"class":"form-control", "placeholder":"iban"}),
            'email': forms.EmailInput(attrs={"type":"email", "class":"form-control", "placeholder":"email"}),
            'numero_contacto': forms.TextInput(attrs={"type":"text", "class":"form-control", "placeholder":"numero contacto"})
                  
        }
        fields = '__all__'

class FormRegistrarBoleta(forms.ModelForm):
    class Meta:
        model = Boleta
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'numero_boleta': forms.TextInput(attrs={"class":"form-control", "placeholder":"numero boleta", "required":"true"}),
            'direccion': forms.TextInput(attrs={"class":"form-control", "placeholder":"direccion"}),
            'fecha_emision': forms.DateInput(attrs={"type":"date","class":"form-control", "required":"true"}),
            'fecha_vencimiento': forms.DateInput(attrs={"type":"date","class":"form-control"}),
            'tipo_boleta': forms.TextInput(attrs={"class":"form-control", "placeholder":"tipo de boleta"}),
            'hora': forms.TextInput(attrs={"class":"form-control", "placeholder":"hora"}),
            'terminal': forms.TextInput(attrs={"class":"form-control", "placeholder":"terminal"}),
            'proveedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"proveedor", "required":"true"}),
            'rut_empresa': forms.TextInput(attrs={"class":"form-control", "placeholder":"rut empresa"}),
            'rut_cliente': forms.TextInput(attrs={"class":"form-control", "placeholder":"rut cliente"}), 
            'cliente': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre cliente"}),
            'nombre_vendedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre vendedor"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "placeholder":"observación", "rows": "3", "maxlength": "600"}), 
            'monto_neto': forms.TextInput(attrs={"class":"form-control", "placeholder":"monto neto", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}), 
            'iva': forms.TextInput(attrs={"class":"form-control", "placeholder":"iva"}), 
            'total': forms.TextInput(attrs={"class":"form-control", "placeholder":"total", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras", "required":"true"}),
            'codigo_klap': forms.TextInput(attrs={"class":"form-control", "placeholder":"codigo klap"}),
            'codigo_autorizacion': forms.TextInput(attrs={"class":"form-control", "placeholder":"codigo de autorización"}),
            'codigo_operacion': forms.TextInput(attrs={"class":"form-control", "placeholder":"codigo de operación"}), 
            'metodo_pago': forms.TextInput(attrs={"class":"form-control", "placeholder":"metodo de pago"}), 

        }
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user')  # Obtener el usuario actual
            super(FormRegistrarBoleta, self).__init__(*args, **kwargs)
            self.fields['nombre_proyecto'].queryset = Proyecto.objects.filter(username=user)


class FormActualizarBoleta(forms.ModelForm):
    class Meta:
        model = Boleta
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput, 
            'numero_boleta': forms.TextInput(attrs={"class":"form-control", "placeholder":"numero boleta", "required":"true"}),
            'direccion': forms.TextInput(attrs={"class":"form-control", "placeholder":"direccion"}),
            'fecha_emision': forms.DateInput(attrs={"type":"date","class":"form-control", "required":"true"}),
            'fecha_vencimiento': forms.DateInput(attrs={"type":"date","class":"form-control"}),
            'tipo_boleta': forms.TextInput(attrs={"class":"form-control", "placeholder":"tipo de boleta"}),
            'hora': forms.TextInput(attrs={"class":"form-control", "placeholder":"hora"}),
            'terminal': forms.TextInput(attrs={"class":"form-control", "placeholder":"terminal"}),
            'proveedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"proveedor", "required":"true"}),
            'rut_empresa': forms.TextInput(attrs={"class":"form-control", "placeholder":"rut empresa"}),
            'rut_cliente': forms.TextInput(attrs={"class":"form-control", "placeholder":"rut cliente"}), 
            'cliente': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre cliente"}),
            'nombre_vendedor': forms.TextInput(attrs={"class":"form-control", "placeholder":"nombre vendedor"}),
            'observacion': forms.Textarea(attrs={"type": "text","class":"form-control", "placeholder":"observación", "rows": "3", "maxlength": "600"}), 
            'monto_neto': forms.TextInput(attrs={"class":"form-control", "placeholder":"monto neto", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}), 
            'iva': forms.TextInput(attrs={"class":"form-control", "placeholder":"iva"}), 
            'total': forms.TextInput(attrs={"class":"form-control", "placeholder":"total", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'codigo_klap': forms.TextInput(attrs={"class":"form-control", "placeholder":"codigo klap"}),
            'codigo_autorizacion': forms.TextInput(attrs={"class":"form-control", "placeholder":"codigo de autorización"}),
            'codigo_operacion': forms.TextInput(attrs={"class":"form-control", "placeholder":"codigo de operación"}), 
            'metodo_pago': forms.TextInput(attrs={"class":"form-control", "placeholder":"metodo de pago"}), 
        }
        fields = '__all__'

class FormAsociarMaterialProyecto(forms.ModelForm):
    class Meta:
        model = AsociarMaterial
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre_proyecto': forms.Select(attrs={"class":"form-select", "placeholder":"nombre proyecto", "required":"true"}),
            'material': forms.Select(attrs={"class":"form-select", "placeholder":"material", "required":"true"}),
            'cantidad': forms.TextInput(attrs={"type":"text","class":"form-control", "placeholder":"cantidad", "required":"true", "min": "1", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
        }
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(FormAsociarMaterialProyecto, self).__init__(*args, **kwargs)
            if user:
                self.fields['nombre_proyecto'].queryset = Proyecto.objects.filter(username=user)
                self.fields['material'].queryset = Materiales.objects.filter(username=user)

class FormActualizarMaterialAsociado(forms.ModelForm):
    class Meta:
        model = AsociarMaterial
        widgets = {
            'estado': forms.HiddenInput,
            'username': forms.HiddenInput,
            'nombre_proyecto': forms.HiddenInput,
            'material': forms.HiddenInput,
            'cantidad': forms.TextInput(attrs={"type":"text","class":"form-control", "placeholder":"cantidad", "required":"true", "min": "1", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
        }
        fields = '__all__'

class FormAsociarFacturaProyecto(forms.ModelForm):
    class Meta:
        model = AsociarFactura
        widgets = {
            'username': forms.HiddenInput,
            'nombre_proyecto': forms.Select(attrs={"class":"form-select", "placeholder":"nombre proyecto", "required":"true"}),
            'numero_factura': forms.Select(attrs={"class":"form-select", "placeholder":"numero_factura", "required":"true"})
                
        }
        fields = '__all__'


    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(FormAsociarFacturaProyecto, self).__init__(*args, **kwargs)
            if user:
                self.fields['nombre_proyecto'].queryset = Proyecto.objects.filter(username=user)
                self.fields['numero_factura'].queryset = Factura.objects.filter(username=user)

class FormAsociarBoletaProyecto(forms.ModelForm):
    class Meta:
        model = AsociarBoleta
        widgets = {
            'username': forms.HiddenInput,
            'nombre_proyecto': forms.Select(attrs={"class":"form-select", "placeholder":"nombre proyecto", "required":"true"}),
            'numero_boleta': forms.Select(attrs={"class":"form-select", "placeholder":"numero_boleta", "required":"true"})
                
        }
        fields = '__all__'


    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(FormAsociarBoletaProyecto, self).__init__(*args, **kwargs)
            if user:
                self.fields['nombre_proyecto'].queryset = Proyecto.objects.filter(username=user)
                self.fields['numero_boleta'].queryset = Boleta.objects.filter(username=user)

class FormAsociarMaestroProyecto(forms.ModelForm):
    class Meta:
        model = AsociarMaestro
        widgets = {
            'username': forms.HiddenInput,
            'nombre_proyecto': forms.Select(attrs={"class":"form-select", "placeholder":"nombre proyecto", "required":"true"}),
            'nombre_maestro': forms.Select(attrs={"class":"form-select", "placeholder":"nombre_maestro", "required":"true"}),
            'trabajo': forms.TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"trabajo maestro"}),
            'saldo_inicial':forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"saldo inicial", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'saldo_a_deber':forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"saldo a deber", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'cobro_maestro': forms.TextInput(attrs={"type":"text", "class":"form-control", "id":"floatingInput", "placeholder":"cobro maestro", "pattern": "[^.,$A-Za-z]+", "title": "Evita los puntos, comas, $ y letras"}),
            'observacion': forms.Textarea(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"observacion", "maxlength": "600"})
                
        }
        fields = '__all__'


    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(FormAsociarMaestroProyecto, self).__init__(*args, **kwargs)
            if user:
                self.fields['nombre_proyecto'].queryset = Proyecto.objects.filter(username=user)
                self.fields['nombre_maestro'].queryset = Maestro.objects.filter(username=user)

########### Contactanos ##############

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)
