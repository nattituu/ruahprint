from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..models import Producto
from ..forms import FormularioContacto


def index(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/publico/index.html', {
        'productos': productos
    })

def detalle_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    # Productos relacionados de la misma categoría
    relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(codigo=codigo)[:4]
    return render(request, 'tienda/publico/detalle_producto.html', {
        'producto': producto,
        'relacionados': relacionados
    })

def ofertas_escolares(request):
    ofertas = Producto.objects.all()[:12]
    return render(request, 'tienda/publico/ofertas.html', {'ofertas': ofertas})

def contacto(request):
    if request.method == 'POST':
        form = FormularioContacto(request.POST)
        if form.is_valid():
            messages.success(request, "¡Gracias! Tu mensaje ha sido enviado. Te contactaremos pronto.")
            return redirect('contacto')
    else:
        form = FormularioContacto()
    return render(request, 'tienda/publico/contacto.html', {'form': form})