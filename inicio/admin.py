from django.contrib import admin
from .models import (
    Operador, 
    Vehiculo, 
    Viaje, 
    BitacoraCarga, 
    GastoViaje, 
    Liquidacion, 
    EvidenciaGasto
)

@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'licencia', 'tipo_licencia', 'estado')
    search_fields = ('nombre', 'licencia')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placas', 'tipo', 'capacidad_carga_toneladas', 'estado')
    search_fields = ('placas', 'tipo')

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'origen', 'destino', 'operador', 'vehiculo', 'fecha_salida', 'estado')
    list_filter = ('estado', 'fecha_salida')
    
@admin.register(BitacoraCarga)
class BitacoraCargaAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'mercancia', 'horario_carga', 'horario_descarga')

@admin.register(GastoViaje)
class GastoViajeAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'tipo_gasto', 'monto', 'fecha')
    list_filter = ('tipo_gasto',)

@admin.register(Liquidacion)
class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'total_a_pagar', 'estado', 'fecha_liquidacion')
    list_filter = ('estado',)

@admin.register(EvidenciaGasto)
class EvidenciaGastoAdmin(admin.ModelAdmin):
    list_display = ('gasto', 'comentario')

# Textos personalizados para el panel de administración
admin.site.site_header = "Panel de Administración - Transportes Santos"
admin.site.site_title = "Portal de Administración"
admin.site.index_title = "Bienvenido al sistema de gestión"