from django.db import models


class Operador(models.Model):
    ESTADOS_OPERADOR = [
        ('activo', 'Activo'),
        ('en_viaje', 'En Viaje'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    licencia = models.CharField(max_length=50, unique=True)
    tipo_licencia = models.CharField(max_length=20)
    estado = models.CharField(
        max_length=20, choices=ESTADOS_OPERADOR, default='activo'
    )

    def __str__(self):
        return f'{self.nombre} (Lic: {self.licencia})'


class Vehiculo(models.Model):
    ESTADOS_VEHICULO = [
        ('disponible', 'Disponible'),
        ('en_ruta', 'En Ruta'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    placas = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=50)  # Tráiler, Torton, Camioneta, etc.
    capacidad_carga_toneladas = models.DecimalField(
        max_digits=5, decimal_places=2
    )
    estado = models.CharField(
        max_length=20, choices=ESTADOS_VEHICULO, default='disponible'
    )

    def __str__(self):
        return f'{self.tipo} - Placas: {self.placas}'


class Viaje(models.Model):
    ESTADOS_VIAJE = [
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    operador = models.ForeignKey(
        Operador, on_delete=models.PROTECT, related_name='viajes'
    )
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT, related_name='viajes'
    )
    fecha_salida = models.DateTimeField()
    fecha_llegada_estimada = models.DateTimeField()
    estado = models.CharField(
        max_length=20, choices=ESTADOS_VIAJE, default='programado'
    )

    def __str__(self):
        return f'Viaje #{self.id}: {self.origen} ➔ {self.destino} ({self.estado})'


class BitacoraCarga(models.Model):
    viaje = models.ForeignKey(
        Viaje, on_delete=models.CASCADE, related_name='bitacoras'
    )
    mercancia = models.CharField(max_length=150)
    horario_carga = models.DateTimeField(null=True, blank=True)
    horario_descarga = models.DateTimeField(null=True, blank=True)
    incidencias = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Bitácora Viaje #{self.viaje.id} - {self.mercancia}'

# ==========================================
# MODELOS DE LA TERCERA ETAPA (FINANZAS)
# ==========================================

class GastoViaje(models.Model):
    TIPOS_GASTO = [
        ('combustible', 'Combustible'),
        ('caseta', 'Caseta'),
        ('viaticos', 'Viáticos'),
        ('reparacion', 'Reparación / Mantenimiento en Ruta'),
        ('otro', 'Otro'),
    ]

    viaje = models.ForeignKey(
        Viaje, on_delete=models.CASCADE, related_name='gastos'
    )
    tipo_gasto = models.CharField(max_length=30, choices=TIPOS_GASTO)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_tipo_gasto_display()} - ${self.monto} (Viaje #{self.viaje.id})'


class Liquidacion(models.Model):
    ESTADOS_LIQUIDACION = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
    ]

    viaje = models.OneToOneField(
        Viaje, on_delete=models.CASCADE, related_name='liquidacion'
    )
    anticipo_otorgado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_gastos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sueldo_operador = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(
        max_length=20, choices=ESTADOS_LIQUIDACION, default='pendiente'
    )
    fecha_liquidacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Liquidación Viaje #{self.viaje.id} - Estado: {self.get_estado_display()}'


class EvidenciaGasto(models.Model):
    gasto = models.ForeignKey(
        GastoViaje, on_delete=models.CASCADE, related_name='evidencias'
    )
    archivo = models.FileField(upload_to='comprobantes_gastos/')
    comentario = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'Evidencia para gasto #{self.gasto.id}'