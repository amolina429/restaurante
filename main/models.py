from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Pedido(models.Model):
    TIPO_SERVICIO = [
        ('MESA', 'Servicio en Mesa'),
        ('DOMICILIO', 'Domicilio'),
        ('RECOGER', 'Recoger en Tienda'),
    ]
    
    TIPO_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('PAS', 'Pasaporte'),
    ]
    
    servicio = models.CharField(max_length=10, choices=TIPO_SERVICIO)
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20)
    nombre_completo = models.CharField(max_length=100)
    celular = models.CharField(max_length=15)
    email = models.EmailField()
    fecha = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    
    # Campos específicos por servicio
    numero_mesa = models.PositiveIntegerField(null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.get_servicio_display()}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    plato = models.ForeignKey('Plato', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    observaciones = models.TextField(blank=True)
    
    @property
    def subtotal(self):
        return self.plato.precio * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    icono = models.CharField(max_length=30, help_text="Nombre del icono de FontAwesome")
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('categoria-list')

class Plato(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='platos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='platos/')
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

    def get_absolute_url(self):
        return reverse('plato-list')