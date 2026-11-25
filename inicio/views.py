import urllib.parse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Operador, Vehiculo, Viaje, BitacoraCarga


def home(request):
    return render(request, 'inicio/index.html')


def historia(request):
    return render(request, 'inicio/historia.html')


def servicios(request):
    return render(request, 'inicio/servicios.html')


def destinos(request):
    return render(request, 'inicio/destinos.html')


def preguntas(request):
    return render(request, 'inicio/preguntas.html')


def cotizacion(request):
    mensaje = None
    url_whatsapp = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        mercancia = request.POST.get('mercancia', '').strip()
        origen = request.POST.get('origen', '').strip()
        destino = request.POST.get('destino', '').strip()
        detalles = request.POST.get('detalles', '').strip()

        if all([nombre, correo, telefono, mercancia, origen, destino]):
            mensaje = f'¡Gracias, {nombre}! Tu solicitud se ha procesado correctamente.'

            # Estructura del mensaje para WhatsApp
            texto_mensaje = (
                f'Hola Transportes Santos, me gustaría solicitar una cotización:\n\n'
                f'📌 *Nombre:* {nombre}\n'
                f'📧 *Correo:* {correo}\n'
                f'📞 *Teléfono:* {telefono}\n'
                f'📦 *Mercancía:* {mercancia}\n'
                f'📍 *Origen:* {origen}\n'
                f'🏁 *Destino:* {destino}\n'
            )
            if detalles:
                texto_mensaje += f'📝 *Detalles:* {detalles}\n'

            # Codificación del texto y generación del enlace de WhatsApp
            texto_encoded = urllib.parse.quote(texto_mensaje)
            numero_whatsapp = '525650041604'
            url_whatsapp = f'https://wa.me/{numero_whatsapp}?text={texto_encoded}'

        else:
            mensaje = 'Por favor, completa todos los campos obligatorios.'

    return render(
        request,
        'inicio/cotizacion.html',
        {'mensaje': mensaje, 'url_whatsapp': url_whatsapp}
    )


@staff_member_required
def operaciones_dashboard(request):
    """Vista exclusiva para administradores que muestra flota, viajes y operadores."""
    viajes = Viaje.objects.all().order_by('-fecha_salida')
    vehiculos = Vehiculo.objects.all()
    operadores = Operador.objects.all()

    contexto = {
        'viajes': viajes,
        'vehiculos': vehiculos,
        'operadores': operadores,
    }
    return render(request, 'inicio/operaciones.html', contexto)