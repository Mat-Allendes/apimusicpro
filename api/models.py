from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
#from settings import AUTH_USER_MODEL

#Clase para el producto
class Producto(models.Model):
    CATEGORIAS_CHOICES = (
        ('Guitarras Cuerpo Solido', 'Guitarras Cuerpo Solido'),
        ('Guitarras Acústicas', 'Guitarras Acústicas'),
        ('Guitarras Eléctricas', 'Guitarras Eléctricas'),
        ('Bajos Cuatro Cuerdas', 'Bajos Cuatro Cuerdas'),
        ('Bajos Cinco Cuerdas', 'Bajos Cinco Cuerdas'),
        ('Bajos Activos', 'Bajos Activos'),
        ('Bajos Pasivos', 'Bajos Pasivos'),
        ('Piano de media cola', 'Piano de media cola'),
        ('Piano de cola entera', 'Piano de cola entera'),
        ('Pianolas', 'Pianolas')
    )
    id = models.AutoField(primary_key=True)
    imagen_url = models.CharField(max_length=200, blank=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    serie = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    descripcion = models.TextField()
    stock = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_CHOICES)

    def __str__(self):
        return self.nombre

#Clase para el usuario
class CustomUser(AbstractUser):
    ROLES_CHOICES = (
        ('administrador', 'Administrador'),
        ('bodeguero', 'Bodeguero'),
    )

    role = models.CharField(max_length=20, choices=ROLES_CHOICES)

    def __str__(self):
        return self.username

#Clase para el grupo
class Meta:
    ordering = ['username']

#Clase para el pedido
class OrdenPedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    productos = models.ManyToManyField(Producto, through='DetalleOrdenPedido')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aceptada = models.BooleanField(default=False)
    despachada = models.BooleanField(default=False)
    def __str__(self):
        return f"Orden de Pedido #{self.pk}"

# Clase para el detalle de un pedido
class DetalleOrdenPedido(models.Model):
    orden_pedido = models.ForeignKey(OrdenPedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto,  related_name='detalles_orden_pedido')
    # Cantidad del producto en el detalle
    cantidad = models.IntegerField()
    def __str__(self):
        return f"Detalle de Orden de Pedido #{self.orden_pedido.pk}"

