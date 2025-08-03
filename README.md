# FoodPlaza API

API RESTful para la gestión de plazas de comida, desarrollada con FastAPI y MySQL.


## 📋 Requisitos

- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd foodplaza-fastapi
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configuración:
   - Copia el archivo `.env.template` a `.env`
   - Configura las variables de entorno según tu entorno local

5. Crea la base de datos en MySQL:
   ```sql
   CREATE DATABASE nombre_de_tu_base_de_datos;
   ```

## 🚦 Ejecución

1. Inicia el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload
   ```

2. La aplicación estará disponible en:
   - API: http://localhost:8000/api
   - Documentación Swagger UI: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc

## 📚 Documentación de la API

La documentación detallada de los endpoints está organizada por módulos:

- [Plazas](docs/api/PLAZAS.md) - Gestión de plazas de comida
- [Locales](docs/api/LOCALES.md) - Gestión de locales dentro de las plazas
- [Menús](docs/api/MENUS.md) - Gestión de menús de los locales
- [Productos](docs/api/PRODUCTOS.md) - Gestión de productos en los menús
- [Pedidos](docs/api/PEDIDOS.md) - Gestión de pedidos de los clientes
- [Usuarios](docs/api/USERS.md) - Gestión de usuarios y autenticación
- [Autenticación](docs/api/AUTHENTICATION.md) - Proceso de autenticación y autorización

## 🧪 Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

## 🛠 Estructura del Proyecto

```
foodplaza-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── db.py                # Configuración de la base de datos
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas/             # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── plazas.py
│   │   ├── locales.py
│   │   ├── menus.py
│   │   ├── productos.py
│   │   ├── pedidos.py
│   │   └── usuarios.py
│   ├── crud/                # Operaciones de base de datos
│   │   ├── __init__.py
│   │   ├── plazas.py
│   │   ├── locales.py
│   │   ├── menus.py
│   │   ├── productos.py
│   │   ├── pedidos.py
│   │   └── usuarios.py
│   ├── routers/             # Rutas de la API
│   │   ├── __init__.py
│   │   ├── plazas.py
│   │   ├── locales.py
│   │   ├── menus.py
│   │   ├── productos.py
│   │   ├── pedidos.py
│   │   └── usuarios.py
│   ├── core/                # Configuraciones centrales
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración de la aplicación
│   │   └── security.py      # Utilidades de seguridad
│   └── utils/               # Utilidades varias
│       ├── __init__.py
│       └── cloudinary.py    # Manejo de imágenes en Cloudinary
├── tests/                  # Pruebas unitarias
├── docs/                   # Documentación
│   └── api/
│       └── PLAZAS.md
├── .env.template           # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```
