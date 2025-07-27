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
  ]
  ```

## Obtener plaza por ID
- **Método**: `GET`
- **Ruta**: `/api/plazas/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID de la plaza
- **Respuestas**:
  - 200 OK: Devuelve la plaza solicitada
    ```json
    {
      "id": 1,
      "nombre": "Plaza Central",
      "direccion": "Av. Principal 123",
      "estado": "activo"
    }
    ```
  - 404 Not Found: Si no se encuentra la plaza

## Crear una nueva plaza
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
- **Respuestas**:
  - 201 Created: Devuelve la plaza creada
  - 400 Bad Request: Si los datos son inválidos

## Actualizar una plaza existente
- **Método**: `PUT`
- **Ruta**: `/api/plazas/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID de la plaza a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Plaza Actualizada",
    "direccion": "Nueva Dirección 789",
    "estado": "inactivo"
  }
  ```
- **Respuestas**:
  - 200 OK: Devuelve la plaza actualizada
  - 400 Bad Request: Si los datos son inválidos
  - 404 Not Found: Si no se encuentra la plaza

## Eliminar una plaza
- **Método**: `DELETE`
- **Ruta**: `/api/plazas/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID de la plaza a eliminar
- **Respuestas**:
  - 204 No Content: Plaza eliminada correctamente
  - 404 Not Found: Si no se encuentra la plaza
