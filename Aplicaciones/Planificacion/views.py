from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importamos el sistema de mensajes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import *
from django.conf import settings
import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from datetime import date



# Create your views here.
def inicio(request):
    return render(request, 'administrador/plantilla-admin.html')

## Rutas para el administrador de Planificacion

def crear_queja(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        detalle = request.POST.get('detalle')
        email = request.POST.get('email')  # Correo al que se enviará el mensaje
        foto = request.FILES.get('foto')

        # Validación de campos obligatorios
        if not nombre or not apellido or not cedula or not detalle or not email:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('crear_queja')

        try:
            # Crear la queja
            queja = Quejas.objects.create(
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                detalle=detalle,
                Email=email,
                foto=foto,
            )

            # Enviar correo automáticamente al email proporcionado
            asunto = f"Detalle de la Queja Registrada: {queja.nombre} {queja.apellido}"
            mensaje = f"""
            Estimado/a {queja.nombre} {queja.apellido},

            Hemos recibido su queja con la siguiente información:
            
            Cédula: {queja.cedula}
            Detalle: {queja.detalle}
            Correo Electrónico: {queja.Email}

            Saludos cordiales,
            Equipo de Soporte
            """
            destinatario = queja.Email

            email_message = EmailMessage(
                subject=asunto,
                body=mensaje,
                from_email=settings.EMAIL_HOST_USER,
                to=[destinatario],
            )

            # Adjuntar la foto si existe
            if foto:
                email_message.attach(foto.name, foto.read(), foto.content_type)

            email_message.send(fail_silently=False)

            messages.success(request, f"Queja registrada correctamente. Se ha enviado un correo a {destinatario}.")
            return redirect('listar_quejas')

        except Exception as e:
            messages.error(request, f"Error al registrar la queja o enviar el correo: {str(e)}")
            return redirect('crear_queja')

    return render(request, 'administrador/crear_queja.html')


# Vista para listar todas las quejas
def listar_quejas(request):
    quejas = Quejas.objects.all()
    return render(request, 'administrador/listar_quejas.html', {'quejas': quejas})
# Vista para mostrar los detalles de una queja específica
def detalle_queja(request, id_queja):
    queja = get_object_or_404(Quejas, id_queja=id_queja)
    return render(request, 'administrador/detalle_queja.html', {'queja': queja})


# Vistas para Viviendas
def crear_vivienda(request):
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        tipo = request.POST.get('tipo')
        estado = request.POST.get('estado')
        id_constructora = request.POST.get('id_constructora')
        id_cliente = request.POST.get('id_cliente')
        foto = request.FILES.get('foto')
        nombre = request.POST.get('nombre')

        if not direccion or not tipo or not estado or not id_constructora:
            messages.error(request, "Todos los campos obligatorios deben ser completados.")
            return redirect('crear_vivienda')

        try:
            constructora = Constructora.objects.get(id_constructora=id_constructora)
            cliente = Cliente.objects.get(id_cliente=id_cliente) if id_cliente else None

            vivienda = Vivienda.objects.create(
                direccion=direccion,
                tipo=tipo,
                estado=estado,
                id_constructora=constructora,
                id_cliente=cliente,
                foto=foto,
                nombre=nombre,
            )

            messages.success(request, f"Vivienda en {vivienda.direccion} creada correctamente.")
            return redirect('listar_viviendas')
        
        except Exception as e:
            messages.error(request, f"Error al crear la vivienda: {str(e)}")
            return redirect('crear_vivienda')

    constructoras = Constructora.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'administrador/crear_vivienda.html', {'constructoras': constructoras, 'clientes': clientes})

def eliminar_vivienda(request, id_vivienda):
    vivienda = get_object_or_404(Vivienda, id_vivienda=id_vivienda)
    try:
        vivienda.delete()
        return JsonResponse({'success': True, 'message': 'Vivienda eliminada correctamente.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error al eliminar la vivienda: {str(e)}'})


def listar_viviendas(request):
    viviendas = Vivienda.objects.all()
    return render(request, 'administrador/listar_viviendas.html', {'viviendas': viviendas})

def detalle_vivienda(request, id_vivienda):
    vivienda = get_object_or_404(Vivienda, id_vivienda=id_vivienda)
    return render(request, 'administrador/detalle_vivienda.html', {'vivienda': vivienda})

def editar_vivienda(request, id_vivienda):
    vivienda = get_object_or_404(Vivienda, id_vivienda=id_vivienda)

    if request.method == 'POST':
        vivienda.direccion = request.POST.get('direccion')
        vivienda.tipo = request.POST.get('tipo')
        vivienda.estado = request.POST.get('estado')
        vivienda.nombre = request.POST.get('nombre')
        vivienda.id_constructora = Constructora.objects.get(id_constructora=request.POST.get('id_constructora'))
        vivienda.id_cliente = Cliente.objects.get(id_cliente=request.POST.get('id_cliente')) if request.POST.get('id_cliente') else None
        
        if request.FILES.get('foto'):
            vivienda.foto = request.FILES.get('foto')

        vivienda.save()
        messages.success(request, "Vivienda actualizada correctamente.")
        return redirect('listar_viviendas')

    # Obtener constructoras y clientes
    constructoras = Constructora.objects.all()
    clientes = Cliente.objects.all()

    return render(request, 'administrador/editar_vivienda.html', {
        'vivienda': vivienda,
        'constructoras': constructoras,
        'clientes': clientes
    })

def eliminar_vivienda(request, id_vivienda):
    vivienda = get_object_or_404(Vivienda, id_vivienda=id_vivienda)
    vivienda.delete()
    messages.success(request, "Vivienda eliminada correctamente.")
    return redirect('listar_viviendas')

# Vistas para Constructoras
def crear_constructora(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        ciudad = request.POST.get('ciudad')
        direccion = request.POST.get('direccion')

        if not nombre or not telefono or not email or not ciudad or not direccion:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('crear_constructora')

        try:
            constructora = Constructora.objects.create(
                nombre=nombre,
                telefono=telefono,
                email=email,
                ciudad=ciudad,
                direccion=direccion
            )
            messages.success(request, f"Constructora {constructora.nombre} creada correctamente.")
            return redirect('listar_constructoras')
        except Exception as e:
            messages.error(request, f"Error al crear la constructora: {str(e)}")
            return redirect('crear_constructora')

    return render(request, 'administrador/crear_constructora.html')

def listar_constructoras(request):
    constructoras = Constructora.objects.all()
    return render(request, 'administrador/listar_constructoras.html', {'constructoras': constructoras})

def detalle_constructora(request, id_constructora):
    constructora = get_object_or_404(Constructora, id_constructora=id_constructora)
    return render(request, 'administrador/detalle_constructora.html', {'constructora': constructora})

def editar_constructora(request, id_constructora):
    constructora = get_object_or_404(Constructora, id_constructora=id_constructora)
    if request.method == 'POST':
        constructora.nombre = request.POST.get('nombre')
        constructora.telefono = request.POST.get('telefono')
        constructora.email = request.POST.get('email')
        constructora.ciudad = request.POST.get('ciudad')
        constructora.direccion = request.POST.get('direccion')
        constructora.save()
        messages.success(request, "Constructora actualizada correctamente.")
        return redirect('listar_constructoras')
    return render(request, 'administrador/editar_constructora.html', {'constructora': constructora})

def eliminar_constructora(request, id_constructora):
    constructora = get_object_or_404(Constructora, id_constructora=id_constructora)
    constructora.delete()
    messages.success(request, "Constructora eliminada correctamente.")
    return redirect('listar_constructoras')

# Vistas para Clientes
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        foto = request.FILES.get('foto')

        if not nombre or not telefono or not email:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('crear_cliente')

        try:
            cliente = Cliente.objects.create(
                nombre=nombre,
                telefono=telefono,
                email=email,
                foto=foto
            )
            messages.success(request, f"Cliente {cliente.nombre} creado correctamente.")
            return redirect('listar_clientes')
        except Exception as e:
            messages.error(request, f"Error al crear el cliente: {str(e)}")
            return redirect('crear_cliente')

    return render(request, 'administrador/crear_cliente.html')

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'administrador/listar_clientes.html', {'clientes': clientes})

def detalle_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    return render(request, 'administrador/detalle_cliente.html', {'cliente': cliente})

def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.telefono = request.POST.get('telefono')
        cliente.email = request.POST.get('email')
        if request.FILES.get('foto'):
            cliente.foto = request.FILES.get('foto')
        cliente.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('listar_clientes')
    return render(request, 'administrador/editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('listar_clientes')

# Vistas para Actividades

def crear_actividad(request):
    today = date.today()  # Obtener la fecha actual en formato YYYY-MM-DD

    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        id_vivienda = request.POST.get('id_vivienda')
        id_constructora = request.POST.get('id_constructora')

        if not descripcion or not fecha_inicio or not fecha_fin or not id_vivienda or not id_constructora:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('crear_actividad')

        try:
            vivienda = Vivienda.objects.get(id_vivienda=id_vivienda)
            constructora = Constructora.objects.get(id_constructora=id_constructora)

            actividad = Actividad.objects.create(
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                id_vivienda=vivienda,
                id_constructora=constructora
            )
            messages.success(request, f"Actividad {actividad.descripcion} creada correctamente.")
            return redirect('listar_actividades')
        except Exception as e:
            messages.error(request, f"Error al crear la actividad: {str(e)}")
            return redirect('crear_actividad')

    viviendas = Vivienda.objects.all()
    constructoras = Constructora.objects.all()

    return render(request, 'administrador/crear_actividad.html', {
        'viviendas': viviendas,
        'constructoras': constructoras,
        'today': today,  # Pasar la fecha al template
    })

def listar_actividades(request):
    actividades = Actividad.objects.all()
    return render(request, 'administrador/listar_actividades.html', {'actividades': actividades})

def detalle_actividad(request, id_actividad):
    actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
    return render(request, 'administrador/detalle_actividad.html', {'actividad': actividad})

def editar_actividad(request, id_actividad):
    actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
    today = date.today()  # Fecha de hoy para el campo 'fecha_fin'
    
    if request.method == 'POST':
        actividad.descripcion = request.POST.get('descripcion')
        actividad.fecha_inicio = request.POST.get('fecha_inicio')  # Fecha de inicio no editable
        actividad.fecha_fin = request.POST.get('fecha_fin')
        actividad.id_vivienda = Vivienda.objects.get(id_vivienda=request.POST.get('id_vivienda'))
        actividad.id_constructora = Constructora.objects.get(id_constructora=request.POST.get('id_constructora'))
        actividad.save()
        messages.success(request, "Actividad actualizada correctamente.")
        return redirect('listar_actividades')

    # Convertir las fechas al formato adecuado para HTML date input
    fecha_inicio = actividad.fecha_inicio.strftime('%Y-%m-%d') if actividad.fecha_inicio else ''
    fecha_fin = actividad.fecha_fin.strftime('%Y-%m-%d') if actividad.fecha_fin else ''

    viviendas = Vivienda.objects.all()
    constructoras = Constructora.objects.all()

    return render(request, 'administrador/editar_actividad.html', {
        'actividad': actividad,
        'viviendas': viviendas,
        'constructoras': constructoras,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'today': today,  # Pasamos la fecha de hoy al template
    })

def eliminar_actividad(request, id_actividad):
    actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
    actividad.delete()
    messages.success(request, "Actividad eliminada correctamente.")
    return redirect('listar_actividades')
