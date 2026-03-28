from django.contrib import admin
# Importamos los modelos que creamos en el paso anterior
from .models import Categoria, Producto, MenuAcceso, Cliente

# Los registramos para que aparezcan en el panel /admin
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(MenuAcceso)
admin.site.register(Cliente)