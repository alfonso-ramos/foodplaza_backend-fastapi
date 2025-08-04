# Manual Técnico

## Presentación

Este manual técnico proporciona información detallada sobre la arquitectura, el diseño y la implementación del sistema FoodPlaza. Está dirigido a desarrolladores, administradores de sistemas y personal técnico que necesite comprender el funcionamiento interno de la aplicación.

## Objetivo

El objetivo de este manual es describir la estructura del sistema, las tecnologías utilizadas y los procesos clave para facilitar el mantenimiento, la extensión y el despliegue de la aplicación.

## Procesos

El sistema gestiona los siguientes procesos principales:

*   **Autenticación de usuarios:** Valida las credenciales de los usuarios y asigna roles (administrador, gerente, usuario).
*   **Gestión de plazas:** Permite a los administradores crear, leer, actualizar y eliminar (CRUD) plazas de comida.
*   **Gestión de locales:** Permite a los administradores y gerentes realizar operaciones CRUD sobre los locales asociados a una plaza.
*   **Gestión de menús y productos:** Permite a los gerentes realizar operaciones CRUD sobre los menús y productos de sus locales.
*   **Gestión de pedidos:** Permite a los usuarios crear y consultar sus pedidos. Los gerentes pueden actualizar el estado de los pedidos.
*   **Gestión de imágenes:** Permite subir y asociar imágenes a plazas, locales y productos, utilizando Cloudinary como servicio de almacenamiento.

## Requisitos del sistema

### Hardware

*   **Servidor:** 2 CPU, 4 GB RAM, 50 GB de almacenamiento.
*   **Cliente:** Navegador web moderno (Chrome, Firefox, Safari, Edge).

### Software

*   **Servidor:** Python 3.9+, Uvicorn, Gunicorn.
*   **Base de datos:** MySQL 8.0+.
*   **Cliente:** No se requieren instalaciones adicionales.

## Herramientas utilizadas para el desarrollo

*   **Backend:** FastAPI
*   **Base de datos:** SQLAlchemy con PyMySQL
*   **Autenticación:** python-jose, passlib
*   **Validación de datos:** Pydantic
*   **Servidor de aplicaciones:** Uvicorn, Gunicorn
*   **Almacenamiento de imágenes:** Cloudinary
*   **Entorno virtual:** venv

## Instalación de aplicaciones

1.  Clonar el repositorio.
2.  Crear y activar un entorno virtual.
3.  Instalar las dependencias: `pip install -r requirements.txt`
4.  Configurar las variables de entorno en un archivo `.env` (basado en `.env.template`).
5.  Ejecutar la aplicación: `uvicorn app.main:app --reload`

## Modelo de clases

*AQUÍ VA EL DIAGRAMA DE CLASES*

## Diagrama de casos de uso

*AQUÍ VA EL DIAGRAMA DE CASOS DE USO*

## Diagrama entidad relación

*AQUÍ VA EL DIAGRAMA ENTIDAD RELACIÓN*

## Diccionario de datos

### Tabla: `plazas`

| Campo            | Tipo         | Tamaño | Descripción                | Clave   |
| ---------------- | ------------ | ------ | -------------------------- | ------- |
| id               | Integer      |        | Identificador único        | Primaria|
| nombre           | String       | 100    | Nombre de la plaza         |         |
| direccion        | String       | 200    | Dirección de la plaza      |         |
| estado           | String       | 20     | Estado (activo/inactivo)   |         |
| imagen_url       | String       | 500    | URL de la imagen           |         |
| imagen_public_id | String       | 500    | ID público de la imagen    |         |

### Tabla: `locales`

| Campo              | Tipo         | Tamaño | Descripción                | Clave   |
| ------------------ | ------------ | ------ | -------------------------- | ------- |
| id                 | Integer      |        | Identificador único        | Primaria|
| nombre             | String       | 100    | Nombre del local           |         |
| descripcion        | String       | 500    | Descripción del local      |         |
| direccion          | String       | 200    | Dirección del local        |         |
| horario_apertura   | String       | 5      | Hora de apertura (HH:MM)   |         |
| horario_cierre     | String       | 5      | Hora de cierre (HH:MM)     |         |
| tipo_comercio      | String       | 50     | Tipo de comercio           |         |
| estado             | String       | 20     | Estado (activo/inactivo)   |         |
| imagen_url         | String       | 500    | URL de la imagen           |         |
| imagen_public_id   | String       | 500    | ID público de la imagen    |         |
| plaza_id           | Integer      |        | ID de la plaza (Foránea)   | Foránea |
| id_gerente         | Integer      |        | ID del gerente (Foránea)   | Foránea |

### Tabla: `usuarios`

| Campo               | Tipo         | Tamaño | Descripción                | Clave   |
| ------------------- | ------------ | ------ | -------------------------- | ------- |
| id                  | Integer      |        | Identificador único        | Primaria|
| nombre              | String       | 100    | Nombre del usuario         |         |
| email               | String       | 100    | Correo electrónico         | Única   |
| telefono            | String       | 20     | Teléfono de contacto       |         |
| password            | String       | 255    | Contraseña hasheada        |         |
| rol                 | String       | 20     | Rol del usuario            |         |
| estado              | String       | 20     | Estado (activo/inactivo)   |         |
| fecha_creacion      | DateTime     |        | Fecha de creación          |         |
| fecha_actualizacion | DateTime     |        | Fecha de actualización     |         |
| imagen_url          | String       | 500    | URL de la imagen           |         |
| imagen_public_id    | String       | 500    | ID público de la imagen    |         |

### Tabla: `pedidos`

| Campo                         | Tipo         | Tamaño | Descripción                | Clave   |
| ----------------------------- | ------------ | ------ | -------------------------- | ------- |
| id                            | Integer      |        | Identificador único        | Primaria|
| id_usuario                    | Integer      |        | ID del usuario (Foránea)   | Foránea |
| id_local                      | Integer      |        | ID del local (Foránea)     | Foránea |
| fecha_pedido                  | DateTime     |        | Fecha del pedido           |         |
| estado_pedido                 | Enum         |        | Estado del pedido          |         |
| total_pedido                  | DECIMAL      | 10, 2  | Total del pedido           |         |
| instrucciones_especiales      | Text         |        | Instrucciones especiales   |         |
| tiempo_preparacion_estimado   | Integer      |        | Tiempo de preparación (min)|         |

### Tabla: `pedido_items`

| Campo                      | Tipo         | Tamaño | Descripción                | Clave   |
| -------------------------- | ------------ | ------ | -------------------------- | ------- |
| id                         | Integer      |        | Identificador único        | Primaria|
| id_pedido                  | Integer      |        | ID del pedido (Foránea)    | Foránea |
| id_producto                | Integer      |        | ID del producto (Foránea)  | Foránea |
| cantidad                   | Integer      |        | Cantidad de productos      |         |
| precio_unitario            | DECIMAL      | 10, 2  | Precio por unidad          |         |
| instrucciones_especiales   | Text         |        | Instrucciones especiales   |         |

### Tabla: `menus`

| Campo         | Tipo         | Tamaño | Descripción                | Clave   |
| ------------- | ------------ | ------ | -------------------------- | ------- |
| id            | Integer      |        | Identificador único        | Primaria|
| id_local      | Integer      |        | ID del local (Foránea)     | Foránea |
| nombre_menu   | String       | 100    | Nombre del menú            |         |
| descripcion   | String       | 255    | Descripción del menú       |         |

### Tabla: `productos`

| Campo            | Tipo         | Tamaño | Descripción                | Clave   |
| ---------------- | ------------ | ------ | -------------------------- | ------- |
| id               | Integer      |        | Identificador único        | Primaria|
| nombre           | String       | 100    | Nombre del producto        |         |
| descripcion      | Text         |        | Descripción del producto   |         |
| precio           | DECIMAL      | 10, 2  | Precio del producto        |         |
| id_menu          | Integer      |        | ID del menú (Foránea)      | Foránea |
| disponible       | Boolean      |        | Disponibilidad del producto|         |
| categoria        | String       | 50     | Categoría del producto     |         |
| imagen_url       | String       | 500    | URL de la imagen           |         |
| imagen_public_id | String       | 500    | ID público de la imagen    |         |
