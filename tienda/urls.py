from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='tienda/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('registrar/', views.registrar, name='registrar'),

    # Productos públicos
    path('producto/<str:codigo>/', views.detalle_producto, name='detalle_producto'),
    path('ofertas-escolares/', views.ofertas_escolares, name='ofertas_escolares'),
    path('contacto/', views.contacto, name='contacto'),

    # Categorías
    path('categorias/', views.listar_categoria, name='listar_categoria'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<str:codigo>/', views.modificar_categoria, name='modificar_categoria'),
    path('categorias/eliminar/<str:codigo>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Gestión productos
    path('gestion/productos/', views.listar_productos, name='listar_productos'),
    path('gestion/productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('gestion/productos/editar/<str:codigo>/', views.editar_producto, name='editar_producto'),
    path('gestion/productos/eliminar/<str:codigo>/', views.eliminar_producto, name='eliminar_producto'),

    # Bodega
    path('gestion/bodega/', views.gestion_bodega, name='gestion_bodega'),
    path('actualizar-stock/<str:codigo>/', views.actualizar_stock, name='actualizar_stock'),

    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<str:codigo>/', views.agregar_producto, name="agregar_carrito"),
    path('carrito/eliminar-item/<str:codigo>/', views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('carrito/actualizar/<str:codigo>/<str:accion>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),

    # API
    path('api/pasarelapago', views.pasarela_pago, name='pasarela_pago'),

    # Pedidos y ventas
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('gestion/ventas/', views.gestion_ventas, name='gestion_ventas'),
    path('gestion/ventas/cambiar-estado/<int:pedido_id>/<str:nombre_estado>/', views.cambiar_estado, name='cambiar_estado'),
    path('gestion/reporte-ventas/', views.reporte_ventas, name='reporte_ventas'),

    # Menú
    path('gestion/menu/', views.listar_menu, name='listar_menu'),
    path('gestion/menu/nuevo/', views.crear_menu, name='crear_menu'),
    path('gestion/menu/editar/<int:id>/', views.editar_menu, name='editar_menu'),
    path('gestion/menu/eliminar/<int:id>/', views.eliminar_menu, name='eliminar_menu'),

    # Usuarios
    path('gestion/usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('gestion/usuarios/nuevo/', views.editar_usuario, name='crear_usuario'),
    path('gestion/usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('gestion/usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Dashboard
    path('gestion/dashboard/', views.dashboard, name='dashboard'),
    path('gestion/stock-critico/<str:codigo>/', views.actualizar_stock_critico, name='actualizar_stock_critico'),
]