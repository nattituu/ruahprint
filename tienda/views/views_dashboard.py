from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from datetime import timedelta
import json

from ..models import (
    Producto, Stock, Pedido, DetallePedido,
    CarritoDB, Cliente
)


@staff_member_required
def dashboard(request):

    productos_criticos = Stock.objects.filter(
        cantidad__lte=F('stock_critico')
    ).select_related('producto')

    top_productos = DetallePedido.objects.values(
        'producto__nombre'
    ).annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:5]

    top_clientes = Pedido.objects.values(
        'cliente__nombre_completo'
    ).annotate(
        total_compras=Sum('total'),
        cantidad_pedidos=Count('id')
    ).order_by('-total_compras')[:5]

    ticket_promedio = Pedido.objects.filter(
        estado__nombre='Pagado'
    ).aggregate(Avg('total'))['total__avg'] or 0

    hace_7_dias = timezone.now() - timedelta(days=7)
    ventas_periodo = Pedido.objects.filter(
        fecha__gte=hace_7_dias,
        estado__nombre='Pagado'
    ).extra(
        select={'dia': 'DATE(fecha)'}
    ).values('dia').annotate(
        total_dia=Sum('total'),
        cantidad=Count('id')
    ).order_by('dia')

    total_carritos = CarritoDB.objects.count()
    carritos_activos = CarritoDB.objects.filter(
        items__isnull=False
    ).distinct().count()
    carritos_abandonados = total_carritos - carritos_activos

    pedidos_pagados = Pedido.objects.filter(estado__nombre='Pagado').count()
    pedidos_pendientes = Pedido.objects.filter(estado__nombre='Pendiente').count()
    total_recaudado = Pedido.objects.filter(
        estado__nombre='Pagado'
    ).aggregate(Sum('total'))['total__sum'] or 0

    productos_vendidos = DetallePedido.objects.values_list('producto__codigo', flat=True).distinct()
    productos_sin_ventas = Producto.objects.exclude(codigo__in=productos_vendidos)

    chart_productos = {
        'labels': [p['producto__nombre'] for p in top_productos],
        'data': [p['total_vendido'] for p in top_productos],
    }

    chart_carritos = {
        'labels': ['Pagados', 'Pendientes', 'Abandonados'],
        'data': [pedidos_pagados, pedidos_pendientes, carritos_abandonados],
    }

    chart_ventas_periodo = {
        'labels': [str(v['dia']) for v in ventas_periodo],
        'data': [v['total_dia'] for v in ventas_periodo],
    }

    context = {
        'productos_criticos': productos_criticos,
        'cantidad_criticos': productos_criticos.count(),

        'top_productos': top_productos,
        'top_clientes': top_clientes,
        'ticket_promedio': round(ticket_promedio),
        'total_recaudado': total_recaudado,
        'pedidos_pagados': pedidos_pagados,
        'pedidos_pendientes': pedidos_pendientes,
        'carritos_abandonados': carritos_abandonados,
        'productos_sin_ventas': productos_sin_ventas,

        'chart_productos': json.dumps(chart_productos),
        'chart_carritos': json.dumps(chart_carritos),
        'chart_ventas_periodo': json.dumps(chart_ventas_periodo),
    }

    return render(request, 'tienda/admin/dashboard.html', context)


@staff_member_required
def actualizar_stock_critico(request, codigo):
    """Permite al admin cambiar el umbral de stock crítico de un producto"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from ..models import Stock

    if request.method == 'POST':
        nuevo_critico = request.POST.get('stock_critico', 5)
        stock = get_object_or_404(Stock, producto__codigo=codigo)
        stock.stock_critico = nuevo_critico
        stock.save()
        messages.success(request, f"Stock crítico actualizado para {stock.producto.nombre}.")
    return redirect('dashboard')