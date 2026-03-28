from .views_auth import registrar
from .views_publico import index, detalle_producto, ofertas_escolares, contacto
from .views_carrito import (
    ver_carrito, agregar_producto, eliminar_del_carrito,
    limpiar_carrito, finalizar_compra, mis_pedidos,
    actualizar_cantidad_carrito
)
from .views_admin import (
    listar_productos, crear_producto, editar_producto, eliminar_producto,
    listar_categoria, crear_categoria, modificar_categoria, eliminar_categoria,
    gestion_bodega, actualizar_stock,
    gestion_ventas, cambiar_estado, reporte_ventas,
    listar_menu, crear_menu, editar_menu, eliminar_menu,
    listar_usuarios, editar_usuario, eliminar_usuario
)
from .views_api import pasarela_pago
from .views_dashboard import dashboard, actualizar_stock_critico