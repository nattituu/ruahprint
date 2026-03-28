from django.db import models
from django.contrib.auth.models import User


class MenuAcceso(models.Model):
    codigo = models.CharField(max_length=50)
    texto = models.CharField(max_length=100)
    perfil = models.CharField(max_length=50)
    padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='hijos'
    )

    class Meta:
        verbose_name = "Acceso de Menú"
        db_table = "tabla_menu_personalizada"

    def __str__(self):
        if self.padre:
            return f"  └─ {self.texto} ({self.perfil})"
        return f"{self.texto} ({self.perfil})"

    def es_padre(self):
        return self.padre is None


class Categoria(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "categoria_productos"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    mail = models.EmailField()

    def __str__(self):
        return self.nombre_completo


class EstadoPedido(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Stock(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='inventario')
    cantidad = models.IntegerField(default=0)
    stock_critico = models.IntegerField(default=5)  # ← NUEVO: umbral configurable por producto

    def __str__(self):
        return f"{self.producto.nombre} - Stock: {self.cantidad}"

    def es_critico(self):
        """Retorna True si el stock está en nivel crítico"""
        return self.cantidad <= self.stock_critico

    def porcentaje_stock(self):
        """Para la barra de progreso visual"""
        if self.stock_critico == 0:
            return 100
        porcentaje = (self.cantidad / (self.stock_critico * 3)) * 100
        return min(porcentaje, 100)


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(EstadoPedido, on_delete=models.PROTECT)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre_completo}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_unitario = models.IntegerField()
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Detalle {self.pedido.id} - {self.producto.nombre}"


class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class CarritoDB(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_cantidad_total(self):
        return sum(item.cantidad for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(CarritoDB, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"

    def get_subtotal(self):
        return self.producto.precio * self.cantidad