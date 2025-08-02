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
    "id_menu": 1
  }
  ```
- **Validaciones**:
  - nombre: obligatorio, máximo 100 caracteres
  - precio: obligatorio, debe ser mayor a 0
  - disponible: opcional, por defecto true
  - id_menu: obligatorio, debe existir el menú
  - categoria: opcional, máximo 50 caracteres
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
      "id_menu": 1
    }
    ```
  - 400 Bad Request: Datos inválidos o faltantes
  - 404 Not Found: Si el menú no existe

## Obtener producto por ID
- **Método**: `GET`
- **Ruta**: `/api/productos/{producto_id}`
- **Parámetros de ruta**:
  - `producto_id` (requerido): ID del producto a buscar
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
      "id_menu": 1
    }
    ```
  - 404 Not Found: Si el producto no existe

## Obtener productos por menú
- **Método**: `GET`
- **Ruta**: `/api/productos/menu/{menu_id}`
- **Parámetros de ruta**:
  - `menu_id` (requerido): ID del menú cuyos productos se quieren obtener
- **Parámetros de consulta**:
  - `skip` (opcional, default: 0): Número de registros a saltar
  - `limit` (opcional, default: 100): Número máximo de registros a devolver
  - `disponible` (opcional): Filtrar por disponibilidad (true/false)
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
      "id_menu": 1
    }
  ]
  ```
  - 404 Not Found: Si el menú no existe

## Actualizar un producto
- **Método**: `PUT`
- **Ruta**: `/api/productos/{producto_id}`
- **Parámetros de ruta**:
  - `producto_id` (requerido): ID del producto a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Hamburguesa Clásica Especial",
    "precio": 109.99,
    "disponible": true,
    "categoria": "Hamburguesas Premium"
  }
  ```
  > **Nota**: Todos los campos son opcionales. Solo se actualizarán los campos proporcionados.
- **Respuestas**:
  - 200 OK: Producto actualizado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "Hamburguesa Clásica Especial",
      "descripcion": "Deliciosa hamburguesa con queso, lechuga y tomate",
      "precio": 109.99,
      "disponible": true,
      "categoria": "Hamburguesas Premium",
      "id_menu": 1
    }
    ```
  - 400 Bad Request: Datos inválidos
  - 404 Not Found: Si el producto no existe

## Eliminar un producto
- **Método**: `DELETE`
- **Ruta**: `/api/productos/{producto_id}`
- **Parámetros de ruta**:
  - `producto_id` (requerido): ID del producto a eliminar
- **Respuestas**:
  - 204 No Content: Producto eliminado exitosamente
  - 404 Not Found: Si el producto no existe

## Subir imagen de un Producto
- **Método**: `POST`
- **Ruta**: `/api/productos/{producto_id}/imagen`
- **Parámetros de ruta**:
  - `producto_id` (requerido): ID del producto al que se le asignará la imagen
- **Cuerpo de la solicitud (form-data)**:
  - `file` (requerido): Archivo de imagen a subir (formatos soportados: jpg, jpeg, png, webp)
- **Descripción**: Sube una imagen para un producto específico. Si el producto ya tiene una imagen, será reemplazada.
- **Respuesta exitosa (200 OK)**:
  ```json
  {
    "url": "https://res.cloudinary.com/.../producto_1.jpg",
    "public_id": "foodplaza/productos/producto_1",
    "mensaje": "Imagen subida exitosamente"
  }
  ```
- **Errores**:
  - 400 Bad Request: Si el archivo no es una imagen
  - 404 Not Found: Si el producto no existe
  - 500 Internal Server Error: Si ocurre un error al procesar la imagen

## Eliminar imagen de un Producto
- **Método**: `DELETE`
- **Ruta**: `/api/productos/{producto_id}/imagen`
- **Parámetros de ruta**:
  - `producto_id` (requerido): ID del producto del que se eliminará la imagen
- **Descripción**: Elimina la imagen asociada a un producto.
- **Respuesta exitosa (200 OK)**:
  ```json
  {
    "mensaje": "Imagen eliminada exitosamente"
  }
  ```
- **Errores**:
  - 404 Not Found: Si el producto no existe o no tiene una imagen asociada
  - 500 Internal Server Error: Si ocurre un error al eliminar la imagen
