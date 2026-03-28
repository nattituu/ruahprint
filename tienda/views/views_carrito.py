import json
import urllib.request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from ..models import Producto, Cliente, Pedido, DetallePedido, EstadoPedido
from ..carrito import Carrito


def ver_carrito(request):
    if not request.user.is_authenticated:
        return redirect('login')
    carrito = Carrito(request)
    return render(request, 'tienda/carrito/carrito_resumen.html', {
        'items': carrito.get_items(),
        'total_carrito': carrito.get_total()
    })

def agregar_producto(request, codigo):
    if not request.user.is_authenticated:
        messages.info(request, "¡Crea una cuenta para guardar tus productos y no perderlos! 🛒")
        return redirect('registrar')
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, codigo=codigo)
    carrito.agregar(producto=producto)
    return redirect("ver_carrito")

def eliminar_del_carrito(request, codigo):
    if not request.user.is_authenticated:
        return redirect('login')
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, codigo=codigo)
    carrito.eliminar(producto=producto)
    return redirect("ver_carrito")

def limpiar_carrito(request):
    if not request.user.is_authenticated:
        return redirect('login')
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("ver_carrito")

@login_required
def finalizar_compra(request):
    carrito = Carrito(request)
    items = carrito.get_items()

    if not items.exists():
        return redirect('index')

    cliente, created = Cliente.objects.get_or_create(
        usuario=request.user,
        defaults={
            'nombre_completo': request.user.username,
            'mail': request.user.email,
            'direccion': 'Dirección por completar',
            'telefono': '00000000'
        }
    )

    estado_inicial = EstadoPedido.objects.get_or_create(nombre="Pendiente")[0]
    total = sum(item.get_subtotal() for item in items)

    try:
        with transaction.atomic():
            nuevo_pedido = Pedido.objects.create(
                usuario=request.user,
                cliente=cliente,
                estado=estado_inicial,
                total=total
            )
            for item in items:
                DetallePedido.objects.create(
                    pedido=nuevo_pedido,
                    producto=item.producto,
                    precio_unitario=item.producto.precio,
                    cantidad=item.cantidad
                )

            payload = json.dumps({
                'pedido_id': nuevo_pedido.id,
                'monto': total
            }).encode('utf-8')

            req = urllib.request.Request(
                'http://localhost:8000/api/pasarelapago',
                data=payload,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req) as response:
                respuesta = json.loads(response.read().decode())

            if respuesta.get('estado') == 'confirmado':
                estado_pagado = EstadoPedido.objects.get_or_create(nombre="Pagado")[0]
                nuevo_pedido.estado = estado_pagado
                nuevo_pedido.save()
                carrito.limpiar()
                return render(request, 'tienda/carrito/compra_exitosa.html', {
                    'pedido': nuevo_pedido,
                    'transaccion': respuesta.get('codigo_transaccion')
                })
            else:
                nuevo_pedido.delete()
                return render(request, 'tienda/carrito/carrito_resumen.html', {
                    'items': carrito.get_items(),
                    'total_carrito': total,
                    'error': '❌ Tu pago fue rechazado por el banco. Intenta nuevamente.'
                })

    except Exception as e:
        return render(request, 'tienda/carrito/carrito_resumen.html', {
            'items': carrito.get_items(),
            'total_carrito': total,
            'error': f'Hubo un problema al procesar tu compra: {str(e)}'
        })

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'tienda/pedidos/mis_pedidos.html', {'pedidos': pedidos})

def actualizar_cantidad_carrito(request, codigo, accion):
    if not request.user.is_authenticated:
        return redirect('login')
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, codigo=codigo)
    items = carrito.get_items()
    item = items.filter(producto=producto).first()
    if item:
        if accion == 'sumar':
            carrito.actualizar(producto, item.cantidad + 1)
        elif accion == 'restar':
            carrito.actualizar(producto, item.cantidad - 1)
    return redirect('ver_carrito')