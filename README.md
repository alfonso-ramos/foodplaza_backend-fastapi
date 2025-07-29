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

La documentación detallada de los endpoints está disponible en [docs/api/PLAZAS.md](docs/api/PLAZAS.md).

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
│   ├── db.py               # Configuración de la base de datos
│   ├── models.py           # Modelos SQLAlchemy
│   ├── schemas/            # Esquemas Pydantic
│   │   ├── __init__.py
│   │   └── plazas.py
│   └── crud/               # Operaciones de base de datos
│       ├── __init__.py
│       └── plazas.py
├── tests/                  # Pruebas unitarias
├── docs/                   # Documentación
│   └── api/
│       └── PLAZAS.md
├── .env.template           # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```
