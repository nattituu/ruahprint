from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Avg

from ..models import (
    Categoria, Producto, MenuAcceso, Stock,
    Pedido, EstadoPedido
)
from ..forms import (
    UsuarioForm, ProductoForm, MenuAccesoForm, CategoriaForm
)



@staff_member_required
def listar_productos(request):
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'tienda/admin/producto_list.html', {'productos': productos})

@staff_member_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            Stock.objects.get_or_create(producto=producto, defaults={'cantidad': 0})
            messages.success(request, "¡Producto creado con éxito!")
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'tienda/admin/crear_producto.html', {'form': form})

@staff_member_required
def editar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/admin/producto_form.html', {'form': form})

@staff_member_required
def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.delete()
    messages.warning(request, "Producto eliminado del inventario.")
    return redirect('listar_productos')



@staff_member_required
def listar_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'tienda/admin/categoria_list.html', {'categorias': categorias})

@staff_member_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categoria')
    else:
        form = CategoriaForm()
    return render(request, 'tienda/admin/categoria_form.html', {'form': form, 'edit': False})

@staff_member_required
def modificar_categoria(request, codigo):
    categoria = get_object_or_404(Categoria, codigo=codigo)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categoria')

@staff_member_required
def eliminar_categoria(request, codigo):
    categoria = get_object_or_404(Categoria, codigo=codigo)
    nombre_cat = categoria.nombre
    categoria.delete()
    messages.warning(request, f"Categoría '{nombre_cat}' eliminada.")
    return redirect('listar_categoria')



@staff_member_required
def gestion_bodega(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/admin/bodega.html', {'productos': productos})

@staff_member_required
def actualizar_stock(request, codigo):
    if request.method == 'POST':
        nueva_cantidad = request.POST.get('cantidad', 0)
        producto = get_object_or_404(Producto, codigo=codigo)
        stock, created = Stock.objects.get_or_create(producto=producto)
        stock.cantidad = nueva_cantidad
        stock.save()
        messages.success(request, f"Stock de {producto.nombre} actualizado correctamente.")
    return redirect('gestion_bodega')



@staff_member_required
def gestion_ventas(request):
    ventas = Pedido.objects.all().order_by('-fecha')
    return render(request, 'tienda/admin/gestion_ventas.html', {'ventas': ventas})

@staff_member_required
def cambiar_estado(request, pedido_id, nombre_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    nuevo_estado, created = EstadoPedido.objects.get_or_create(nombre=nombre_estado)
    pedido.estado = nuevo_estado
    pedido.save()
    messages.info(request, f"Pedido #{pedido_id} actualizado a {nombre_estado}.")
    return redirect('gestion_ventas')

@staff_member_required
def reporte_ventas(request):
    total_dinero = Pedido.objects.filter(estado__nombre='Pagado').aggregate(Sum('total'))['total__sum'] or 0
    cantidad_pedidos = Pedido.objects.count()
    ticket_promedio = Pedido.objects.aggregate(Avg('total'))['total__avg'] or 0
    ventas_por_estado = Pedido.objects.values('estado__nombre').annotate(total=Count('id'))
    context = {
        'total_dinero': total_dinero,
        'cantidad_pedidos': cantidad_pedidos,
        'ticket_promedio': ticket_promedio,
        'ventas_por_estado': ventas_por_estado,
    }
    return render(request, 'tienda/admin/reporte_ventas.html', context)



@staff_member_required
def listar_menu(request):
    items = MenuAcceso.objects.all()
    return render(request, 'tienda/admin/menu_list.html', {'items': items})

@staff_member_required
def crear_menu(request):
    if request.method == 'POST':
        form = MenuAccesoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ítem de menú creado.")
            return redirect('listar_menu')
    else:
        form = MenuAccesoForm()
    return render(request, 'tienda/admin/menu_form.html', {'form': form})

@staff_member_required
def editar_menu(request, id):
    item = get_object_or_404(MenuAcceso, id=id)
    if request.method == 'POST':
        form = MenuAccesoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Ítem de menú actualizado.")
            return redirect('listar_menu')
    else:
        form = MenuAccesoForm(instance=item)
    return render(request, 'tienda/admin/menu_form.html', {'form': form})

@staff_member_required
def eliminar_menu(request, id):
    item = get_object_or_404(MenuAcceso, id=id)
    item.delete()
    messages.warning(request, "Ítem de menú eliminado.")
    return redirect('listar_menu')



@staff_member_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'tienda/admin/usuario_list.html', {'usuarios': usuarios})

@staff_member_required
def editar_usuario(request, id=None):
    usuario = get_object_or_404(User, id=id) if id else None
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'tienda/admin/usuario_form.html', {'form': form})

@staff_member_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if usuario != request.user:
        usuario.delete()
        messages.success(request, "Usuario eliminado.")
    else:
        messages.error(request, "No puedes eliminar tu propio usuario.")
    return redirect('listar_usuarios')