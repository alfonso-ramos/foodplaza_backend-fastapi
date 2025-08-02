# API de Plazas

## Listar Plazas
- **Método**: `GET`
- **Ruta**: `/api/plazas`
- **Parámetros de consulta**:
  - `skip` (opcional, default: 0): Número de registros a saltar
  - `limit` (opcional, default: 100): Número máximo de registros a devolver
- **Descripción**: Obtiene un listado paginado de todas las plazas registradas.
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Plaza Central",
      "direccion": "Av. Principal 123",
      "estado": "activo"
    }
  ]
  ```

## Obtener una Plaza
- **Método**: `GET`
- **Ruta**: `/api/plazas/{plaza_id}`
- **Parámetros de ruta**:
  - `plaza_id` (requerido): ID de la plaza a consultar
- **Descripción**: Obtiene los detalles de una plaza específica.
- **Respuesta exitosa (200 OK)**:
  ```json
  {
    "id": 1,
    "nombre": "Plaza Central",
    "direccion": "Av. Principal 123",
    "estado": "activo"
  }
  ```
- **Error (404 Not Found)**:
  ```json
  {
    "detail": "Plaza no encontrada"
  }
  ```

## Crear una Plaza
- **Método**: `POST`
- **Ruta**: `/api/plazas`
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Nueva Plaza",
    "direccion": "Calle Nueva 456",
    "estado": "activo"
  }
  ```
- **Campos requeridos**:
  - `nombre` (string): Nombre de la plaza
  - `direccion` (string): Dirección de la plaza
  - `estado` (string, opcional): Estado de la plaza (default: "activo")
- **Respuesta exitosa (201 Created)**:
  ```json
  {
    "id": 2,
    "nombre": "Nueva Plaza",
    "direccion": "Calle Nueva 456",
    "estado": "activo"
  }
  ```

## Actualizar una Plaza
- **Método**: `PUT`
- **Ruta**: `/api/plazas/{plaza_id}`
- **Parámetros de ruta**:
  - `plaza_id` (requerido): ID de la plaza a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Plaza Actualizada",
    "direccion": "Calle Actualizada 789",
    "estado": "inactivo"
  }
  ```
- **Respuesta exitosa (200 OK)**:
  ```json
  {
    "id": 1,
    "nombre": "Plaza Actualizada",
    "direccion": "Calle Actualizada 789",
    "estado": "inactivo"
  }
  ```
- **Error (404 Not Found)**:
  ```json
  {
    "detail": "Plaza no encontrada"
  }
  ```

## Eliminar una Plaza
- **Método**: `DELETE`
- **Ruta**: `/api/plazas/{plaza_id}`
- **Parámetros de ruta**:
  - `plaza_id` (requerido): ID de la plaza a eliminar
- **Respuesta exitosa (204 No Content)**: Sin contenido
- **Error (404 Not Found)**:
  ```json
  {
    "detail": "Plaza no encontrada"
  }
  ```

## Subir imagen de una Plaza
- **Método**: `POST`
- **Ruta**: `/api/plazas/{plaza_id}/imagen`
- **Parámetros de ruta**:
  - `plaza_id` (requerido): ID de la plaza a la que se le asignará la imagen
- **Cuerpo de la solicitud (form-data)**:
  - `file` (requerido): Archivo de imagen a subir (formatos soportados: jpg, jpeg, png, webp)
- **Descripción**: Sube una imagen para una plaza específica. Si la plaza ya tiene una imagen, será reemplazada.
- **Respuesta exitosa (200 OK)**:
  ```json
  {
    "url": "https://res.cloudinary.com/.../plaza_1.jpg",
    "public_id": "foodplaza/plazas/plaza_1",
    "mensaje": "Imagen subida exitosamente"
  }
  ```
- **Errores**:
  - 400 Bad Request: Si el archivo no es una imagen
  - 404 Not Found: Si la plaza no existe
  - 500 Internal Server Error: Si ocurre un error al procesar la imagen

## Eliminar imagen de una Plaza
- **Método**: `DELETE`
- **Ruta**: `/api/plazas/{plaza_id}/imagen`
- **Parámetros de ruta**:
  - `plaza_id` (requerido): ID de la plaza de la que se eliminará la imagen
- **Descripción**: Elimina la imagen asociada a una plaza.
- **Respuesta exitosa (200 OK)**:
  ```json
  {
    "mensaje": "Imagen eliminada exitosamente"
  }
  ```
- **Errores**:
  - 404 Not Found: Si la plaza no existe o no tiene una imagen asociada
  - 500 Internal Server Error: Si ocurre un error al eliminar la imagen
