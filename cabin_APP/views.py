from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.conf import settings
from django.contrib.auth.views import PasswordResetCompleteView, LoginView
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm 
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login


def planes_precios(request):
    return render(request, 'planes_precios.html')

@login_required
def cambiar_nombre_usuario(request):
    if request.method == 'POST':
        nuevo_nombre = request.POST['nuevo_nombre']

        # Verificar si el nuevo nombre de usuario ya existe
        if User.objects.filter(username=nuevo_nombre).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            user = request.user
            user.username = nuevo_nombre
            user.save()

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Cambio de nombre usuario",
                details=f"El usuario {request.user.username} cambio su nombre de usuario."
            )

            messages.success(request, 'Nombre de usuario cambiado exitosamente.')
            return redirect(main_menu)  

    return render(request, 'cambiar_nombre.html')

@login_required
def cambiar_email(request):
    if request.method == 'POST':
        nuevo_email = request.POST['nuevo_email']

        # Verificar si el nuevo email de usuario ya existe
        if User.objects.filter(email=nuevo_email).exists():
            messages.error(request, 'El email ya está en uso.')
        else:
            user = request.user
            user.email = nuevo_email
            user.save()

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Cambio de email",
                details=f"El usuario {request.user.username} cambio su email."
            )

            messages.success(request, 'Email cambiado exitosamente.')
            return redirect(main_menu)  

    return render(request, 'cambiar_email.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión del usuario

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Cambio de contraseña",
                details=f"El usuario {request.user.username} cambio su contraseña."
            )

            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect(main_menu)  # Redirecciona a la página deseada después del cambio de contraseña
        else:
            messages.error(request, 'No se completo el cambio de contraseña.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'cambiar_contrasenea.html', {'form': form})

@login_required
def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            
            # Enviar el correo electrónico
            subject = f'Nuevo mensaje de contacto de {nombre}'
            message = f'Nombre: {nombre}\nCorreo Electrónico: {email}\nMensaje: {mensaje}'
            from_email = 'dominatuproyecto@gmail.com'  
            recipient_list = ['dominatuproyecto@gmail.com'] 

            send_mail(subject, message, from_email, recipient_list)

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Envio de Email",
                details=f"El usuario {request.user.username} envio un correo a 'Domina_tu_proyecto'"
            )

            messages.success(request,"Correo enviado con exito")
            return render(request, 'contactanos.html') 
        
        else:
            messages.error(request, "El correo no se pudo enviar correctamente")
            return render(request, 'contactanos.html')
    else:
        form = ContactForm()

    return render(request, 'contactanos.html', {'form': form})

@login_required
def template_navbar(request):
    return render(request, 'navbar.html')


def registrarse(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()

            messages.success(request, 'Usuario registrado con exito.')
            return redirect(main_menu)
        else:
            messages.error(request, 'El nombre de usuario ya existe.')

    else:
        form = FormUser()

    data = {
        'form': form
    }
    return render(request, 'registro.html', data)

@login_required
def salir(request):
    logout(request)
    return redirect(index)

def index(request):
    return render(request, 'index.html')

@login_required
def main_menu(request):
    return render(request, 'menu_principal.html')

@login_required
def menu_proyecto_maestros(request):
    return render(request, 'menuProyectoMaestros.html')

@login_required
def menu_factura_boleta(request):
    return render(request, 'menuBoletaFactura.html')

########################PROYECTOS#########################

@login_required
def vista_proyecto(request, id):
    try:
        proyecto = Proyecto.objects.get(id=id)
        materiales = Materiales.objects.filter(username=request.user, estado='Activo')
        boletas = AsociarBoleta.objects.filter(nombre_proyecto=proyecto).select_related('numero_boleta')
        asociaciones = AsociarMaterial.objects.filter(nombre_proyecto=proyecto, estado='Activo').select_related('material')
        facturas = AsociarFactura.objects.filter(nombre_proyecto=proyecto).select_related('numero_factura')
        maestro = AsociarMaestro.objects.filter(nombre_proyecto=proyecto, nombre_maestro__estado='Activo').select_related('nombre_maestro')
        # Usamos select_related para obtener los campos en una sola consulta eficiente
    except Proyecto.DoesNotExist:
        messages.error(request, "El proyecto no existe")
        return redirect('listar_proyecto')
    
    total_precio_materiales = 0
    total_precio_maestro = 0

    for asociacion in asociaciones:
        if asociacion.material and asociacion.material.precio is not None:
            total_precio_materiales += asociacion.cantidad * asociacion.material.precio

    for maestros in maestro:
        if maestros.cobro_maestro is not None:
            total_precio_maestro += maestros.cobro_maestro

    proyecto.costo_termino = total_precio_materiales + total_precio_maestro
    proyecto.save()  # Guardar el proyecto con el costo calculado

    total_general = proyecto.costo_termino  # Calcula el total general (materiales + maestro)

    data = {
        'proyecto': proyecto,
        'materiales': materiales,
        'asociaciones': asociaciones,
        'facturas': facturas,
        'boletas': boletas,
        'maestro': maestro,
        'total_precio_materiales': total_precio_materiales,
        'total_precio_maestro': total_precio_maestro,
        'total_general': total_general  # Agregar el total general al contexto
    }
    return render(request, 'vista_proyecto.html', data)

@login_required
def registrar_proyecto(request):
    form = FormCreateProject(initial={'username': request.user})
    if request.method == 'POST':

        form = FormCreateProject(request.POST, initial={'username': request.user})
        if request.user.id != int(form.data['username']):
            return redirect(registrar_proyecto)

        if form.is_valid():
            form.save()

            nombre_proyecto = form.cleaned_data['nombre']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Registro de proyecto",
                details=f"El usuario {request.user.username} registró el proyecto {nombre_proyecto}."
            )

            messages.success(request,"Proyecto agregado correctamente")
            return render(request, 'registrar_proyecto.html')
        else:
            return redirect('error')

    return render(request, 'registrar_proyecto.html', {'form': form})

# Listamos proyectos creados
@login_required
def listar_proyecto(request):
    proyectos_activos = Proyecto.objects.filter(username=request.user, estado='Activo')

    search_query = request.GET.get('search')
    if search_query:
        proyectos_activos = proyectos_activos.filter(nombre__icontains=search_query)
    
    # Verificar si existen resultados de búsqueda
    resultados_existentes = proyectos_activos.exists()

    data = {
        'proyecto': proyectos_activos,
        'resultados_existentes': resultados_existentes
        }

    return render(request, 'listado_proyecto.html', data)

@login_required
def actualizar_proyecto(request, id):
    try:
        proyecto = Proyecto.objects.get(id=id)

        fe = proyecto.fecha_inicio

        if fe:

            if fe.day >= 1 and fe.day <= 9:
                dia_compra = "0" + str(fe.day)
            else:
                dia_compra = str(fe.day)
                
            if fe.month >= 1 and fe.month <= 9:
                mes_compra = "0" + str(fe.month)
            else:
                mes_compra = str(fe.month)

            fecha_inicio = str(fe.year) + "-" + mes_compra + "-" + dia_compra
        
        else:
            fecha_inicio = None

        ft = proyecto.fecha_termino

        if ft:

            if ft.day >= 1 and ft.day <= 9:
                dia_compra = "0" + str(ft.day)
            else:
                dia_compra = str(ft.day)
                
            if fe.month >= 1 and fe.month <= 9:
                mes_compra = "0" + str(ft.month)
            else:
                mes_compra = str(ft.month)

            fecha_termino = str(ft.year) + "-" + mes_compra + "-" + dia_compra
        
        else:
            fecha_termino = None
        
    except Proyecto.DoesNotExist:
        # Manejar el caso cuando no se encuentra ningun proyecto con el ID dado
        messages.error(request, "El proyecto no existe")
        return redirect('listar_proyecto')
    
    form = FormActualizarProyecto(instance=proyecto)
    if request.method == 'POST':
        form = FormActualizarProyecto(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()

            nombre_proyecto = form.cleaned_data['nombre']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Actualización de proyecto",
                details=f"El usuario {request.user.username} actualizo el proyecto {nombre_proyecto}."
            )

            messages.success(request,"Proyecto actualizado correctamente")
            return redirect(listar_proyecto)
        else:
            return redirect('error')
    else:
        fecha_inicio = fecha_inicio if fecha_inicio else None
        fecha_termino = fecha_termino if fecha_termino else None

        form = FormActualizarProyecto(instance=proyecto, initial={'fecha_inicio': fecha_inicio, 'fecha_termino': fecha_termino})

    proyecto = Proyecto.objects.filter(username=request.user)
    data = {
        'form': form,
        'proyecto': proyecto,
        'fecha_inicio' : fecha_inicio,
        'fecha_termino' : fecha_termino,
    }
    return render(request, 'actualizar_proyecto.html', data)

@login_required
def eliminar_proyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)

    proyecto.estado = 'Eliminado'
    proyecto.save()

    nombre_proyecto = proyecto.nombre

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de proyecto",
        details=f"El usuario {request.user.username} eliminó el proyecto {nombre_proyecto}."
    )
    
    # Realizar la devolución de materiales asociados al proyecto
    asociaciones = AsociarMaterial.objects.filter(nombre_proyecto=proyecto)

    for asociacion in asociaciones:
        asociacion.material.cantidad_disponible += asociacion.cantidad
        asociacion.material.save()

    asociaciones.delete()

    messages.success(request, "Proyecto eliminado correctamente.")
    return redirect(listar_proyecto)

########################MAESTROS#########################
@login_required
def registrar_maestro(request):

    if request.method == 'POST':
        form = FormRegistrarMaestro(request.POST, initial={'username': request.user})
        if form.is_valid():
            maestro = form.save(commit=False)
            maestro.username = request.user
            maestro.save()

            nombre_maestro = form.cleaned_data['nombre']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Registro de maestro",
                details=f"El usuario {request.user.username} registro al maestro {nombre_maestro}."
            )

            messages.success(request, "Maestro agregado correctamente")
            return redirect('registrar_maestro')
        else:
            return redirect('error')
    else:
        form = FormRegistrarMaestro(initial={'username': request.user})

    return render(request, 'registrar_maestro.html', {'form': form})


@login_required
def listar_maestro(request):
    proyectos_usuario = Proyecto.objects.filter(username=request.user, estado='Activo')
    maestros_activos = Maestro.objects.filter(username=request.user, estado='Activo')  
    maestroA = AsociarMaestro.objects.filter(username=request.user)
    search_query = request.GET.get('search')
    if search_query:
        maestros_activos = maestros_activos.filter(nombre__icontains=search_query)
    
    # Verificar si existen resultados de búsqueda
    resultados_existentes = maestros_activos.exists()

    if request.method == 'POST':
        form = FormAsociarMaestroProyecto(request.POST, user=request.user)

        if form.is_valid():
            nombre_maestro = form.cleaned_data['nombre_maestro']
            nombre_proyecto = form.cleaned_data['nombre_proyecto']
            
            # Verificar si el maestro ya está asociado al proyecto
            proyecto_existente = get_object_or_404(Proyecto, id=nombre_proyecto.id)
            if maestroA.filter(nombre_proyecto=proyecto_existente, nombre_maestro=nombre_maestro).exists():
                messages.error(request, "El maestro ya está asociado al proyecto.")
                return redirect('listar_maestro')
            
            maestro = form.save(commit=False)
            maestro.username = request.user
            maestro.save()

            messages.success(request, "Maestro asociado correctamente")
            return redirect('listar_maestro')

        else:
            print(form.errors)
            return redirect('error')
    else:
        form = FormAsociarMaestroProyecto(user=request.user)

    form.fields['nombre_proyecto'].queryset = proyectos_usuario
    form.fields['nombre_maestro'].queryset = maestros_activos  # Solo mostrar maestros activos en el formulario

    data = {
        'maestros_activos': maestros_activos,
        'proyectos_usuario': proyectos_usuario,
        'form': form,
        'maestroA': maestroA,
        'resultados_existentes': resultados_existentes
    }
    
    return render(request, 'listar_maestro.html', data)

@login_required
def eliminar_maestro(request, id):
    maestro = Maestro.objects.get(id=id)

    # Actualizar el estado del maestro a 'Eliminado'
    maestro.estado = 'Eliminado'
    maestro.save()

    nombre_maestro = maestro.nombre

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de maestro",
        details=f"El usuario {request.user.username} eliminó al maestro {nombre_maestro}."
    )

    messages.success(request, "Maestro eliminado correctamente")
    return redirect(listar_maestro)
    
@login_required
def actualizar_maestro(request, id):
    try:
        maestro = Maestro.objects.get(id=id)
        
    except Maestro.DoesNotExist:
        # Manejar el caso cuando no se encuentra ningun material con el ID dado
        messages.error(request, "El maestro no existe")
        return redirect('listar_maestro')
    
    form = FormActualizarMaestro(instance=maestro, user=request.user)  # Pasar el parámetro 'user'
    if request.method == 'POST':
        form = FormActualizarMaestro(request.POST, instance=maestro, user=request.user)  # Pasar el parámetro 'user'
        if form.is_valid():
            form.save()

            nombre_maestro = form.cleaned_data['nombre']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Actualización de maestro",
                details=f"El usuario {request.user.username} actualizó al maestro {nombre_maestro}."
            )

            messages.success(request, "Maestro actualizado correctamente")
            return redirect('listar_maestro')
        else:
            return redirect('error')
    maestro = Maestro.objects.filter(username=request.user)
    data = {
        'form': form,
        'maestro': maestro
    }
    return render(request, 'actualizar_maestro.html', data)


#########################Material############################

@login_required
def registrar_material(request):
    facturas_usuario = Factura.objects.filter(username=request.user, estado='Activo')
    boletas_usuario = Boleta.objects.filter(username=request.user, estado='Activo')

    if request.method == 'POST':
        form = FormRegistrarMaterial(request.POST, initial={'username': request.user})

        if form.is_valid():
            material = form.save(commit=False)

            # Asignar cantidad a cantidad_disponible
            material.cantidad_disponible = material.cantidad
            material.total = material.precio * material.cantidad

            material.username = request.user
            material.save()

            nombre_material = form.cleaned_data['nombre']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Registro de materiales",
                details=f"El usuario {request.user.username} registró el material {nombre_material}."
            )

            messages.success(request, "Material agregado correctamente")
            return redirect('registrar_material')
        else:
            return redirect('error')
    else:
        form = FormRegistrarMaterial(initial={'username': request.user})

    form.fields['facturas'].queryset = facturas_usuario
    form.fields['boletas'].queryset = boletas_usuario

    return render(request, 'registrar_material.html', {'form': form})



@login_required
def listar_materiales(request):
    materiales = Materiales.objects.filter(username=request.user, estado='Activo')
    proyectos_usuario = Proyecto.objects.filter(username=request.user, estado='Activo')

    search_query = request.GET.get('search')
    if search_query:
        materiales = materiales.filter(nombre__icontains=search_query)

    # Verificar si existen resultados de búsqueda
    resultados_existentes = materiales.exists()

    if request.method == 'POST':
        form = FormAsociarMaterialProyecto(request.POST, user=request.user)

        if form.is_valid():
            material_seleccionado = form.cleaned_data['material']
            cantidad_seleccionada = form.cleaned_data['cantidad']
            proyecto_seleccionado = form.cleaned_data['nombre_proyecto']

            # Verificar si el material ya está asociado al proyecto
            asociacion_existente = AsociarMaterial.objects.filter(
                username=request.user,
                material=material_seleccionado,
                nombre_proyecto=proyecto_seleccionado
            ).first()

            if asociacion_existente:
                # Validar si la cantidad excede la cantidad disponible
                if cantidad_seleccionada > material_seleccionado.cantidad_disponible:
                    mensaje_error = "La cantidad seleccionada excede la cantidad disponible del material."
                    messages.error(request, mensaje_error)
                    data = {
                        'materiales': materiales,
                        'form': form,
                        'mensaje_error': mensaje_error,
                        'resultados_existentes': resultados_existentes
                    }
                    return render(request, 'listar_materiales.html', data)

                # Actualizar la cantidad asociada
                asociacion_existente.cantidad += cantidad_seleccionada
                asociacion_existente.save()
            else:
                # Validar si la cantidad excede la cantidad disponible
                if cantidad_seleccionada > material_seleccionado.cantidad_disponible:
                    mensaje_error = "La cantidad seleccionada excede la cantidad disponible del material."
                    messages.error(request, mensaje_error)
                    data = {
                        'materiales': materiales,
                        'form': form,
                        'mensaje_error': mensaje_error,
                        'resultados_existentes': resultados_existentes
                    }
                    return render(request, 'listar_materiales.html', data)

                # Crear una nueva asociación
                asociacion = form.save(commit=False)
                asociacion.username = request.user
                asociacion.save()

            # Actualizar la cantidad disponible en Materiales
            material_seleccionado.cantidad_disponible -= cantidad_seleccionada
            material_seleccionado.save()

            messages.success(request, "Material asociado correctamente")
            return redirect('listar_materiales')

        else:
            print(form.errors)
            return redirect('error')
    else:
        form = FormAsociarMaterialProyecto(user=request.user)

    form.fields['nombre_proyecto'].queryset = proyectos_usuario
    form.fields['material'].queryset = materiales

    data = {
        'materiales': materiales,
        'form': form,
        'resultados_existentes': resultados_existentes
    }

    return render(request, 'listar_materiales.html', data)

@login_required
def actualizar_material(request, id):
    try:
        material = Materiales.objects.get(id=id)
        facturas_usuario = Factura.objects.filter(username=request.user, estado='Activo')
        boletas_usuario = Boleta.objects.filter(username=request.user, estado='Activo')
        mensaje_error_cantidad = None
        
        fe = material.fecha_compra

        if fe:

            if fe.day >= 1 and fe.day <= 9:
                dia_compra = "0" + str(fe.day)
            else:
                dia_compra = str(fe.day)
                
            if fe.month >= 1 and fe.month <= 9:
                mes_compra = "0" + str(fe.month)
            else:
                mes_compra = str(fe.month)

            fecha_compra = str(fe.year) + "-" + mes_compra + "-" + dia_compra
        
        else:
            fecha_compra = None
        
        cd = material.cantidad_disponible
        cantidad = material.cantidad

        form = FormActualizarMaterial(instance=material)

        if request.method == 'POST':
            form = FormActualizarMaterial(request.POST, instance=material)
            if form.is_valid():
                nueva_cantidad = form.cleaned_data['cantidad']
                nuevo_precio = form.cleaned_data['precio']
                material = form.save(commit=False)
                material.username = request.user
                material.total = nuevo_precio * nueva_cantidad

                if cantidad > nueva_cantidad:
                    cantidad_absoluta = cantidad - nueva_cantidad
                    cantidad_disponible = cd - cantidad_absoluta

                    if cantidad_disponible < 0:
                        mensaje_error_cantidad = "La cantidad disponible no puede ser menor que 0."
                        messages.error(request, mensaje_error_cantidad)
                        return redirect('listar_materiales')
                    else:
                        # Actualizar la cantidad disponible y redirigir con mensaje de éxito
                        material.cantidad_disponible = cantidad_disponible
                        material.save()
                        messages.success(request, "Material actualizado correctamente")
                        return redirect('listar_materiales')
                else:
                    cantidad_absoluta = nueva_cantidad - cantidad
                    cantidad_disponible = cd + cantidad_absoluta

                material.cantidad_disponible = cantidad_disponible
                material.save()

                nombre_material = form.cleaned_data['nombre']

                ActivityLog.objects.create(
                    user=request.user,
                    activity_type="Actualización de material",
                    details=f"El usuario {request.user.username} actualizó el material {nombre_material}."
                )

                messages.success(request, "Material actualizado correctamente")
                return redirect('listar_materiales')
            else:
                messages.error(request, "La cantidad seleccionada es mayor que la cantidad disponible")
                return redirect('error')
        
        else:
            fecha_compra = fecha_compra if fecha_compra else None
            form = FormActualizarMaterial(instance=material, initial={'fecha_compra': fecha_compra, 'cantidad_disponible': cd})

        form.fields['facturas'].queryset = facturas_usuario
        form.fields['boletas'].queryset = boletas_usuario
        material = Materiales.objects.filter(username=request.user)
        
        data = {
            'form': form,
            'material': material,
            'fecha_compra': fecha_compra,
            'cantidad_disponible': cd,
            'mensaje_error_cantidad': mensaje_error_cantidad
        }
        return render(request, 'actualizar_material.html', data)
    
    except Materiales.DoesNotExist:
        messages.error(request, "El material no existe")
        return redirect('listar_materiales')


@login_required
def eliminar_material(request, id):
    material = Materiales.objects.get(id=id)
    
    # Cambiar el estado del material a 'Eliminado'
    material.estado = 'Eliminado'
    material.save()

    nombre_material = material.nombre

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de material",
        details=f"El usuario {request.user.username} eliminó el material {nombre_material}."
    )

    # Actualizar el estado de los materiales asociados en el modelo AsociarMaterial
    asociaciones = AsociarMaterial.objects.filter(material=material)
    for asociacion in asociaciones:
        asociacion.estado = 'Eliminado'
        asociacion.save()

    messages.success(request, "Material eliminado correctamente")
    return redirect('listar_materiales')

###################Factura######################
@login_required
def vista_factura(request, id):
    factura = Factura.objects.get(id=id)
    materiales = factura.materiales_set.all()  # Obtener los materiales asociados a la factura

    data = {
        'factura': factura,
        'materiales': materiales
    }
    return render(request, 'vista_factura.html', data)

@login_required
def registrar_factura(request):

    if request.method == 'POST':
        form = FormRegistrarFactura(request.POST, initial={'username': request.user})

        if form.is_valid():
            factura = form.save(commit=False)
            factura.username = request.user
            factura.save()

            numero_factura = form.cleaned_data['numero_factura']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Registro de factura",
                details=f"El usuario {request.user.username} registró la factura N° {numero_factura}."
            )

            messages.success(request, "Factura registrada correctamente")
            return redirect('registrar_factura')
        else:
            return redirect('error')
    else:
        form = FormRegistrarFactura(initial={'username': request.user, 'user': request.user})

    return render(request, 'registrar_factura.html', {'form': form})


@login_required
def listar_factura(request):
    factura = Factura.objects.filter(username=request.user, estado='Activo')
    proyecto = Proyecto.objects.filter(username=request.user, estado='Activo')
    facturaA = AsociarFactura.objects.filter(username=request.user)

    search_query = request.GET.get('search')
    if search_query:
        factura = factura.filter(numero_factura__icontains=search_query)
    
    # Verificar si existen resultados de búsqueda
    resultados_existentes = factura.exists()

    if request.method == 'POST':
        form = FormAsociarFacturaProyecto(request.POST, user=request.user)

        if form.is_valid():
            numero_factura = form.cleaned_data['numero_factura']
            nombre_proyecto = form.cleaned_data['nombre_proyecto']
            
            # Verificar si la factura ya está asociada al proyecto
            proyecto_existente = get_object_or_404(Proyecto, id=nombre_proyecto.id)
            if facturaA.filter(nombre_proyecto=proyecto_existente, numero_factura=numero_factura).exists():
                messages.error(request, "Esta factura ya está asociada al proyecto seleccionado.")
                return redirect('listar_factura')
            
            factura = form.save(commit=False)
            factura.username = request.user
            factura.save()

            messages.success(request, "Factura asociada correctamente")
            return redirect('listar_factura')

        else:
            print(form.errors)
            return redirect('error')
    else:
        form = FormAsociarFacturaProyecto(user=request.user)

    form.fields['nombre_proyecto'].queryset = proyecto
    form.fields['numero_factura'].queryset = factura

    data = {'factura': factura,
            'facturaA': facturaA,
            'form': form,
            'resultados_existentes': resultados_existentes}
    
    return render(request, 'listar_factura.html', data)

@login_required
def actualizar_factura(request, id):
    try:
        factura = Factura.objects.get(id=id)

        fe = factura.fecha_emision

        if fe:

            if fe.day >= 1 and fe.day <= 9:
                dia_emision = "0" + str(fe.day)
            else:
                dia_emision = str(fe.day)
                
            if fe.month >= 1 and fe.month <= 9:
                mes_emision = "0" + str(fe.month)
            else:
                mes_emision = str(fe.month)

            fecha_emision = str(fe.year) + "-" + mes_emision + "-" + dia_emision
        
        else:
            fecha_emision = None
        
        fv = factura.fecha_vencimiento

        if fv:

            if fv.day >= 1 and fv.day <= 9:
                dia_vencimiento = "0" + str(fv.day)
            else:
                dia_vencimiento = str(fv.day)

            if fv.month >= 1 and fv.month <= 9:
                mes_vencimiento = "0" + str(fv.month)
            else:
                mes_vencimiento = str(fv.month)

            fecha_vencimiento = str(fv.year) + "-" + mes_vencimiento + "-" + dia_vencimiento
        
        else:
            fecha_vencimiento = None

    except Factura.DoesNotExist:
        # Manejar el caso cuando no se encuentra ninguna factura con el ID dado
        messages.error(request, "La factura no existe")
        return redirect('listar_factura')

    if request.method == 'POST':
        form = FormActualizarFactura(request.POST, instance=factura)
        form.user = request.user  # Asignar manualmente el atributo 'user' al formulario
        if form.is_valid():
            form.save()

            numero_factura = form.cleaned_data['numero_factura']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Actualización de factura",
                details=f"El usuario {request.user.username} actualizó la factura N° {numero_factura}."
            )

            messages.success(request, "Factura actualizada correctamente")
            return redirect('listar_factura')
        else:
            return redirect('error')
    else:
        fecha_emision = fecha_emision if fecha_emision else None
        fecha_vencimiento = fecha_vencimiento if fecha_vencimiento else None

        form = FormActualizarFactura(instance=factura, initial={'fecha_emision': fecha_emision, 'fecha_vencimiento': fecha_vencimiento})

    data = {
        'form': form,
        'factura': factura,
        'fecha_emision' : fecha_emision,
        'fecha_vencimiento': fecha_vencimiento
    }

    return render(request, 'actualizar_factura.html', data)

@login_required
def eliminar_factura(request, id):
    factura = Factura.objects.get(id=id)

    factura.estado = 'Eliminado'
    factura.save()

    numero_factura = factura.numero_factura

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de factura",
        details=f"El usuario {request.user.username} Elimino la factura {numero_factura}."
    )

    messages.success(request,"Factura eliminada correctamente")
    return redirect(listar_factura)


#############BOLETA################
@login_required
def vista_boleta(request, id):
    boleta = Boleta.objects.get(id=id)
    materiales = boleta.materiales_set.all()  # Obtener los materiales asociados a la boleta
    data = {
        'boleta': boleta,
        'materiales': materiales
    }

    return render(request, 'vista_boleta.html', data)

@login_required
def registrar_boleta(request):

    if request.method == 'POST':
        form = FormRegistrarBoleta(request.POST, initial={'username': request.user})

        if form.is_valid():
            boleta = form.save(commit=False)
            boleta.username = request.user
            boleta.save()

            numero_boleta = form.cleaned_data['numero_boleta']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Registro de boleta",
                details=f"El usuario {request.user.username} registro la boleta N° {numero_boleta}."
            )

            messages.success(request, "Boleta registrada correctamente")
            return redirect('registrar_boleta')
        else:
            return redirect('error')
    else:
        form = FormRegistrarBoleta(initial={'username': request.user, 'user': request.user})

    return render(request, 'registrar_boleta.html', {'form': form})

@login_required
def listar_boleta(request):
    boleta = Boleta.objects.filter(username=request.user, estado='Activo')
    proyecto = Proyecto.objects.filter(username=request.user, estado='Activo')
    boletaA = AsociarBoleta.objects.filter(username=request.user)

    search_query = request.GET.get('search')
    if search_query:
        boleta = boleta.filter(numero_boleta__icontains=search_query)
    
    # Verificar si existen resultados de búsqueda
    resultados_existentes = boleta.exists()

    if request.method == 'POST':
        form = FormAsociarBoletaProyecto(request.POST, user=request.user)

        if form.is_valid():
            numero_boleta = form.cleaned_data['numero_boleta']
            nombre_proyecto = form.cleaned_data['nombre_proyecto']
            
            # Verificar si la boleta ya está asociada al proyecto
            proyecto_existente = get_object_or_404(Proyecto, id=nombre_proyecto.id)
            if boletaA.filter(nombre_proyecto=proyecto_existente, numero_boleta=numero_boleta).exists():
                messages.error(request, "Esta boleta ya está asociada al proyecto seleccionado.")
                return redirect('listar_boleta')
            
            boleta = form.save(commit=False)
            boleta.username = request.user
            boleta.save()

            messages.success(request, "Boleta asociada correctamente")
            return redirect('listar_boleta')

        else:
            print(form.errors)
            return redirect('error')
    else:
        form = FormAsociarBoletaProyecto(user=request.user)

    form.fields['nombre_proyecto'].queryset = proyecto
    form.fields['numero_boleta'].queryset = boleta

    data = {'boleta': boleta,
            'form': form,
            'boletaA': boletaA,
            'resultados_existentes': resultados_existentes}
    
    return render(request, 'listar_boleta.html', data)

@login_required
def actualizar_boleta(request, id):
    try:
        boleta = Boleta.objects.get(id=id)

        fe = boleta.fecha_emision

        if fe:

            if fe.day >= 1 and fe.day <= 9:
                dia_emision = "0" + str(fe.day)
            else:
                dia_emision = str(fe.day)
                
            if fe.month >= 1 and fe.month <= 9:
                mes_emision = "0" + str(fe.month)
            else:
                mes_emision = str(fe.month)

            fecha_emision = str(fe.year) + "-" + mes_emision + "-" + dia_emision
        
        else:
            fecha_emision = None
        
        fv = boleta.fecha_vencimiento

        if fv:

            if fv.day >= 1 and fv.day <= 9:
                dia_vencimiento = "0" + str(fv.day)
            else:
                dia_vencimiento = str(fv.day)

            if fv.month >= 1 and fv.month <= 9:
                mes_vencimiento = "0" + str(fv.month)
            else:
                mes_vencimiento = str(fv.month)

            fecha_vencimiento = str(fv.year) + "-" + mes_vencimiento + "-" + dia_vencimiento
        
        else:
            fecha_vencimiento = None


    except Boleta.DoesNotExist:
        # Manejar el caso cuando no se encuentra ninguna factura con el ID dado
        messages.error(request, "La boleta no existe")
        return redirect('listar_boleta')

    if request.method == 'POST':
        form = FormActualizarBoleta(request.POST, instance=boleta)
        
        form.user = request.user  # Asignar manualmente el atributo 'user' al formulario
        if form.is_valid():
            form.save()

            numero_boleta = form.cleaned_data['numero_boleta']

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Actualización de boleta",
                details=f"El usuario {request.user.username} actualizó la boleta N° {numero_boleta}."
            )

            messages.success(request, "Boleta actualizada correctamente")
            return redirect('listar_boleta')
        else:
            return redirect('error')
    else:
        fecha_emision = fecha_emision if fecha_emision else None
        fecha_vencimiento = fecha_vencimiento if fecha_vencimiento else None
        
        # Aquí pasamos el valor de fecha como parte del argumento initial
        form = FormActualizarBoleta(instance=boleta, initial={'fecha_emision': fecha_emision, 'fecha_vencimiento': fecha_vencimiento})

    data = {
        'form': form,
        'boleta': boleta,
        'fecha_emision' : fecha_emision,
        'fecha_vencimiento': fecha_vencimiento
    }

    return render(request, 'actualizar_boleta.html', data)

@login_required
def eliminar_boleta(request, id):
    boleta = Boleta.objects.get(id=id)
    
    boleta.estado='Eliminado'
    boleta.save()

    numero_boleta = boleta.numero_boleta

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de boleta",
        details=f"El usuario {request.user.username} eliminó la boleta N° {numero_boleta}."
    )

    messages.success(request,"Boleta eliminada correctamente")
    return redirect(listar_boleta)

###########Asociaciones#######################################

@login_required
def actualizar_material_asociado(request, id):
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('nueva_cantidad'))
        asociacion = get_object_or_404(AsociarMaterial, id=id)
        cantidad_anterior = asociacion.cantidad  # Guardamos la cantidad anterior

        # Validar que la nueva cantidad no sea mayor que la cantidad en Materiales
        cantidad_materiales = asociacion.material.cantidad
        if nueva_cantidad > cantidad_materiales:
            messages.error(request, "La cantidad no puede ser mayor que la cantidad del material asociado")
            return redirect('vista_proyecto', id=asociacion.nombre_proyecto.id)

        else:
            # Actualizamos la cantidad_disponible en Materiales antes de cambiar la cantidad en la asociación
            material = asociacion.material
            nueva_cantidad_disponible = material.cantidad_disponible + cantidad_anterior - nueva_cantidad

            if nueva_cantidad_disponible < 0:
                messages.error(request, "La cantidad disponible del material asociado no puede ser menor a 0")
                return redirect('vista_proyecto', id=asociacion.nombre_proyecto.id)

            material.cantidad_disponible = nueva_cantidad_disponible
            material.save()

            # Actualizamos la cantidad en la asociación
            asociacion.cantidad = nueva_cantidad
            asociacion.save()

            # Registro de actividad
            nombre_material_asociado = asociacion.material
            proyecto_asociado = asociacion.nombre_proyecto

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Actualizacion de material asociado",
                details=f"El usuario {request.user.username} actualizó el material {nombre_material_asociado} asociado al proyecto {proyecto_asociado}."
            )
            messages.success(request, "Material actualizado correctamente")

        return redirect('vista_proyecto', id=asociacion.nombre_proyecto.id)

    
@login_required
def actualizar_maestro_asociado(request, id):
    if request.method == 'POST':
        nuevo_trabajo = request.POST.get('nuevo_trabajo')
        nuevo_cobro = request.POST.get('nuevo_cobro')
        nueva_observacion = request.POST.get('nueva_observacion')
        nuevo_saldo_inicial = request.POST.get('nuevo_saldo_inicial')
        nuevo_saldo_adeber = request.POST.get('nuevo_saldo_adeber')

        try:
            maestro_asociado = AsociarMaestro.objects.get(id=id)
            maestro_asociado.trabajo = nuevo_trabajo
            maestro_asociado.cobro_maestro = nuevo_cobro
            maestro_asociado.observacion = nueva_observacion
            maestro_asociado.saldo_inicial = nuevo_saldo_inicial
            maestro_asociado.saldo_a_deber = nuevo_saldo_adeber
            maestro_asociado.save()

            nombre_maestro_asociado = maestro_asociado.nombre_maestro
            proyecto_asociado = maestro_asociado.nombre_proyecto

            ActivityLog.objects.create(
                user=request.user,
                activity_type="Actualizacion de maestro asociado",
                details=f"El usuario {request.user.username} actualizó el maestro {nombre_maestro_asociado} asociado al proyecto {proyecto_asociado}."
            )

            messages.success(request,"Maestro actualizado correctamente")

        except AsociarMaestro.DoesNotExist:
            messages.error(request, "El maestro no existe")
            return redirect('vista_proyecto')

        # Obtén el proyecto_id desde el objeto maestro_asociado
        proyecto_id = maestro_asociado.nombre_proyecto.id

    return redirect('vista_proyecto', id=proyecto_id) 

@login_required
def eliminar_material_asociado(request, id):
    material = AsociarMaterial.objects.get(id=id)
    material.delete()

    nombre_material_asociado = material.material
    proyecto_asociado = material.nombre_proyecto

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de material asociado",
        details=f"El usuario {request.user.username} eliminó el material {nombre_material_asociado} asociado al proyecto {proyecto_asociado}."
    )

    messages.success(request, "material eliminado con exito")
    return redirect('vista_proyecto', id=material.nombre_proyecto.id)

@login_required
def eliminar_factura_asociada(request, id):
    factura = AsociarFactura.objects.get(id=id)
    factura.delete()

    numero_factura_asociada = factura.numero_factura
    proyecto_asociado = factura.nombre_proyecto

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de factura asociada",
        details=f"El usuario {request.user.username} eliminó la factura N° {numero_factura_asociada} asociado al proyecto {proyecto_asociado}."
    )
    
    messages.success(request,"Factura eliminada correctamente")
    return redirect('vista_proyecto', id=factura.nombre_proyecto.id)

@login_required
def eliminar_boleta_asociada(request, id):
    boleta = AsociarBoleta.objects.get(id=id)
    boleta.delete()

    numero_boleta_asociada = boleta.numero_boleta
    proyecto_asociado = boleta.nombre_proyecto

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de boleta asociada",
        details=f"El usuario {request.user.username} eliminó la boleta N° {numero_boleta_asociada} asociado al proyecto {proyecto_asociado}."
    )
    
    messages.success(request,"Boleta eliminada correctamente")
    return redirect('vista_proyecto', id=boleta.nombre_proyecto.id)

@login_required
def eliminar_maestro_asociado(request, id):
    maestro = AsociarMaestro.objects.get(id=id)
    maestro.delete()

    nombre_maestro_asociado = maestro.nombre_maestro
    proyecto_asociado = maestro.nombre_proyecto

    ActivityLog.objects.create(
        user=request.user,
        activity_type="Eliminación de maestro asociado",
        details=f"El usuario {request.user.username} eliminó el maestro {nombre_maestro_asociado} asociado al proyecto {proyecto_asociado}."
    )
    
    messages.success(request,"Maestro eliminado correctamente")
    return redirect('vista_proyecto', id=maestro.nombre_proyecto.id)

#############Historial usuario########################

@login_required
def historial_actividad(request):
    # Recupera el historial de actividad del usuario actual
    activity_log = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, 'historial_usuario.html', {'activity_log': activity_log})


#############Error########################

@login_required
def error(request):
    return render(request, 'error.html')


