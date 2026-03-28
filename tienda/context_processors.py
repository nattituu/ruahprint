from .models import MenuAcceso

def menu_context(request):
    if request.user.is_authenticated and request.user.is_staff:
        menu_items = MenuAcceso.objects.filter(padre=None)
    elif request.user.is_authenticated:
        menu_items = MenuAcceso.objects.filter(perfil__in=['cliente', 'publico'], padre=None)
    else:
        menu_items = MenuAcceso.objects.filter(perfil='publico', padre=None)
    return {'menu_items': menu_items}


def carrito_contador(request):
    """Ahora lee la cantidad desde la BD en vez de la sesión"""
    cantidad = 0
    if request.user.is_authenticated:
        try:
            from .models import CarritoDB
            carrito = CarritoDB.objects.get(usuario=request.user)
            cantidad = carrito.get_cantidad_total()
        except:
            cantidad = 0
    return {"carrito_cantidad": cantidad}