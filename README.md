# 🏷️ Ruah Print — E-commerce de Etiquetas Escolares

E-commerce desarrollado con **Django** y **PostgreSQL** como proyecto de portafolio. Permite a clientes explorar y comprar etiquetas personalizadas, y a administradores gestionar productos, inventario, ventas y más.

---

## 🚀 Tecnologías utilizadas

- **Backend:** Python 3 + Django
- **Base de datos:** PostgreSQL
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Autenticación:** Django Auth + JWT (pasarela)
- **Otros:** Django ORM, Chart.js, context processors

---

## ⚙️ Requisitos e instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ruahprint.git
cd ruahprint
```

### 2. Crear y activar entorno virtual
```bash
python -m venv env

# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos
Crea una base de datos PostgreSQL llamada `ecommers_db` y configura las credenciales en `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommers_db',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Aplicar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor
```bash
python manage.py runserver
```

Abre el navegador en **http://localhost:8000**

---

## 🗺️ Rutas principales

### Públicas
| URL | Descripción |
|-----|-------------|
| `/` | Inicio — catálogo de productos |
| `/producto/<codigo>/` | Detalle de producto |
| `/ofertas-escolares/` | Página de ofertas |
| `/contacto/` | Formulario de contacto |
| `/login/` | Iniciar sesión |
| `/registrar/` | Crear cuenta |

### Cliente (requiere login)
| URL | Descripción |
|-----|-------------|
| `/carrito/` | Ver carrito de compras |
| `/carrito/agregar/<codigo>/` | Agregar producto al carrito |
| `/carrito/finalizar/` | Confirmar y pagar |
| `/mis-pedidos/` | Historial de pedidos |

### Administrador (requiere is_staff)
| URL | Descripción |
|-----|-------------|
| `/gestion/productos/` | Gestión de productos |
| `/gestion/bodega/` | Control de inventario |
| `/gestion/ventas/` | Gestión de ventas |
| `/gestion/reporte-ventas/` | Reporte ejecutivo |
| `/gestion/dashboard/` | Dashboard analytics |
| `/gestion/usuarios/` | Gestión de usuarios |
| `/gestion/menu/` | Configuración del menú |
| `/categorias/` | Gestión de categorías |
| `/api/pasarelapago` | API pasarela de pago |

---

## 👤 Credenciales de prueba

### Administrador
| Campo | Valor |
|-------|-------|
| Usuario | `natta` |
| Contraseña | `tu_password_aqui` |

### Cliente
| Campo | Valor |
|-------|-------|
| Usuario | `cliente_prueba` |
| Contraseña | `Cliente2026.` |

---

## ✨ Funcionalidades principales

- ✅ Autenticación con roles (Admin / Cliente)
- ✅ Catálogo de productos con detalle individual
- ✅ Carrito persistente en base de datos
- ✅ Pasarela de pago simulada (API REST)
- ✅ Historial de pedidos por usuario
- ✅ Panel de administración completo
- ✅ Dashboard analytics con gráficos
- ✅ Stock crítico con alertas visuales
- ✅ Menú dinámico con submenús administrables
- ✅ Validaciones en formularios

---

## 📁 Estructura del proyecto

```
portafolio/
├── ecommerce_escolar/      ← Configuración del proyecto
│   ├── settings.py
│   └── urls.py
├── tienda/                 ← App principal
│   ├── views/              ← Vistas separadas por módulo
│   │   ├── views_auth.py
│   │   ├── views_publico.py
│   │   ├── views_carrito.py
│   │   ├── views_admin.py
│   │   ├── views_api.py
│   │   └── views_dashboard.py
│   ├── forms/              ← Formularios separados por módulo
│   │   ├── forms_auth.py
│   │   ├── forms_productos.py
│   │   ├── forms_admin.py
│   │   └── forms_publico.py
│   ├── templates/tienda/   ← Templates organizados por sección
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── publico/
│   │   ├── carrito/
│   │   ├── admin/
│   │   └── pedidos/
│   ├── models.py
│   ├── carrito.py
│   ├── context_processors.py
│   └── urls.py
├── static/css/
│   └── estilos.css
├── media/                  ← Imágenes de productos
├── requirements.txt
└── manage.py
```

---

## 📸 Capturas de pantalla

### Inicio — Catálogo
![Inicio](capturas/inicio.png)

### Carrito de compras
![Carrito](capturas/carrito.png)

### Dashboard Analytics
![Dashboard](capturas/dashboard.png)

### Panel de administración
![Admin](capturas/admin.png)

---

## 👩‍💻 Desarrollado por

**Natalia** — Trainee en Desarrollo Web  
Proyecto de portafolio — Módulo 8