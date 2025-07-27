# Productos

## Crear un nuevo producto
- **Método**: `POST`
- **Ruta**: `/api/productos`
- **Descripción**: Crea un nuevo producto en el sistema.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Hamburguesa Clásica",
    "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
    "precio": 99.99,
    "disponible": true,
    "categoria": "Hamburguesas",
    "idMenu": 1
  }
  ```
- **Validaciones**:
  - nombre: obligatorio, máximo 100 caracteres
  - precio: obligatorio, debe ser mayor a 0
  - disponible: opcional, por defecto true
  - idMenu: obligatorio, debe existir el menú
- **Respuestas**:
  - 201 Created: Producto creado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica",
      "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
      "precio": 99.99,
      "disponible": true,
      "categoria": "Hamburguesas",
      "idMenu": 1
    }
    ```
  - 400 Bad Request: Datos inválidos o faltantes
  - 404 Not Found: Si el menú no existe

## Obtener todos los productos
- **Método**: `GET`
- **Ruta**: `/api/productos`
- **Descripción**: Obtiene un listado de todos los productos.
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica",
      "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
      "precio": 99.99,
      "disponible": true,
      "categoria": "Hamburguesas",
      "idMenu": 1
    }
  ]
  ```

## Obtener producto por ID
- **Método**: `GET`
- **Ruta**: `/api/productos/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del producto a buscar
- **Respuestas**:
  - 200 OK: Devuelve el producto solicitado
    ```json
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica",
      "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
      "precio": 99.99,
      "disponible": true,
      "categoria": "Hamburguesas",
      "idMenu": 1
    }
    ```
  - 404 Not Found: Producto no encontrado

## Obtener productos por menú
- **Método**: `GET`
- **Ruta**: `/api/productos/menu/{idMenu}`
- **Parámetros de ruta**:
  - `idMenu` (requerido): ID del menú
- **Respuestas**:
  - 200 OK: Lista de productos del menú
    ```json
    [
      {
        "id": 1,
        "nombre": "Hamburguesa Clásica",
        "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
        "precio": 99.99,
        "disponible": true,
        "categoria": "Hamburguesas",
        "idMenu": 1
      }
    ]
    ```
  - 404 Not Found: Si el menú no existe

## Obtener productos por categoría
- **Método**: `GET`
- **Ruta**: `/api/productos/categoria/{categoria}`
- **Parámetros de ruta**:
  - `categoria` (requerido): Nombre de la categoría
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica",
      "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
      "precio": 99.99,
      "disponible": true,
      "categoria": "Hamburguesas",
      "idMenu": 1
    }
  ]
  ```

## Obtener productos disponibles
- **Método**: `GET`
- **Ruta**: `/api/productos/disponibles`
- **Descripción**: Obtiene un listado de productos marcados como disponibles.
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica",
      "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
      "precio": 99.99,
      "disponible": true,
      "categoria": "Hamburguesas",
      "idMenu": 1
    }
  ]
  ```

## Actualizar un producto
- **Método**: `PUT`
- **Ruta**: `/api/productos/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del producto a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Hamburguesa Clásica Especial",
    "descripcion": "Hamburguesa con doble carne, queso, lechuga y tomate",
    "precio": 129.99,
    "disponible": true,
    "categoria": "Hamburguesas Especiales",
    "idMenu": 1
  }
  ```
- **Respuestas**:
  - 200 OK: Producto actualizado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica Especial",
      "descripcion": "Hamburguesa con doble carne, queso, lechuga y tomate",
      "precio": 129.99,
      "disponible": true,
      "categoria": "Hamburguesas Especiales",
      "idMenu": 1
    }
    ```
  - 400 Bad Request: Datos inválidos
  - 404 Not Found: Producto o menú no encontrado

## Eliminar un producto
- **Método**: `DELETE`
- **Ruta**: `/api/productos/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del producto a eliminar
- **Respuestas**:
  - 200 OK: Producto eliminado exitosamente
    ```json
    {
      "success": true,
      "message": "Producto eliminado exitosamente"
    }
    ```
  - 404 Not Found: Producto no encontrado

## Buscar productos por nombre
- **Método**: `GET`
- **Ruta**: `/api/productos/buscar`
- **Parámetros de consulta**:
  - `nombre` (requerido): Texto para buscar en el nombre del producto
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica",
      "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
      "precio": 99.99,
      "disponible": true,
      "categoria": "Hamburguesas",
      "idMenu": 1
    }
  ]
  ```
