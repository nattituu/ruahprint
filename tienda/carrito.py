from .models import CarritoDB, ItemCarrito

class Carrito:
    def __init__(self, request):
        self.request = request
        self.usuario = request.user

    def _get_carrito(self):
        """Obtiene o crea el carrito del usuario en la BD"""
        carrito, creado = CarritoDB.objects.get_or_create(usuario=self.usuario)
        return carrito

    def agregar(self, producto):
        """Agrega un producto o incrementa su cantidad"""
        carrito = self._get_carrito()
        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto
        )
        if not creado:
            item.cantidad += 1
            item.save()

    def actualizar(self, producto, cantidad):
        """Actualiza la cantidad de un producto en el carrito"""
        carrito = self._get_carrito()
        try:
            item = ItemCarrito.objects.get(carrito=carrito, producto=producto)
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()  # Si cantidad es 0, elimina el item
        except ItemCarrito.DoesNotExist:
            pass

    def eliminar(self, producto):
        """Elimina un producto del carrito"""
        carrito = self._get_carrito()
        ItemCarrito.objects.filter(carrito=carrito, producto=producto).delete()

    def limpiar(self):
        """Vacía el carrito completo"""
        carrito = self._get_carrito()
        carrito.items.all().delete()

    def get_items(self):
        """Retorna todos los items del carrito"""
        carrito = self._get_carrito()
        return carrito.items.select_related('producto').all()

    def get_total(self):
        """Retorna el total del carrito"""
        return self._get_carrito().get_total()

    def get_cantidad(self):
        """Retorna la cantidad total de productos"""
        return self._get_carrito().get_cantidad_total()