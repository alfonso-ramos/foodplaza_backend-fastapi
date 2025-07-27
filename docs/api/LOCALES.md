# Locales

## Obtener todos los locales
- **Método**: `GET`
- **Ruta**: `/api/locales`
- **Descripción**: Obtiene un listado de todos los locales registrados.
- **Parámetros de consulta**:
  - `plaza_id` (opcional): Filtrar locales por ID de plaza
  - `estado` (opcional): Filtrar por estado (activo/inactivo)
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Local 1",
      "descripcion": "Descripción del local",
      "direccion": "Dirección del local",
      "horario_apertura": "09:00",
      "horario_cierre": "22:00",
      "estado": "activo",
      "plaza_id": 1
    }
  ]
  ```

## Obtener local por ID
- **Método**: `GET`
- **Ruta**: `/api/locales/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del local
- **Respuestas**:
  - 200 OK: Devuelve el local solicitado
    ```json
    {
      "id": 1,
      "nombre": "Local 1",
      "descripcion": "Descripción del local",
      "direccion": "Dirección del local",
      "horario_apertura": "09:00",
      "horario_cierre": "22:00",
      "estado": "activo",
      "plaza_id": 1
    }
    ```
  - 404 Not Found: Si no se encuentra el local

## Crear un nuevo local
- **Método**: `POST`
- **Ruta**: `/api/locales`
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Nuevo Local",
    "descripcion": "Descripción del nuevo local",
    "direccion": "Dirección del local",
    "horario_apertura": "09:00",
    "horario_cierre": "22:00",
    "estado": "activo",
    "plaza_id": 1
  }
  ```
- **Respuestas**:
  - 201 Created: Local creado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "Nuevo Local",
      "descripcion": "Descripción del nuevo local",
      "direccion": "Dirección del local",
      "horario_apertura": "09:00",
      "horario_cierre": "22:00",
      "estado": "activo",
      "plaza_id": 1
    }
    ```
  - 400 Bad Request: Datos de entrada inválidos o formato de hora incorrecto (debe ser HH:MM)
  - 404 Not Found: La plaza especificada no existe

## Actualizar un local existente
- **Método**: `PUT`
- **Ruta**: `/api/locales/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del local a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Local Actualizado",
    "descripcion": "Nueva descripción",
    "direccion": "Nueva dirección",
    "horario_apertura": "10:00",
    "horario_cierre": "23:00",
    "estado": "activo",
    "plaza_id": 2
  }
  ```
- **Respuestas**:
  - 200 OK: Devuelve el local actualizado
  - 400 Bad Request: Si los datos son inválidos
  - 404 Not Found: Si no se encuentra el local o la plaza

## Eliminar un local
- **Método**: `DELETE`
- **Ruta**: `/api/locales/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del local a eliminar
- **Respuestas**:
  - 204 No Content: Local eliminado correctamente
  - 404 Not Found: Si no se encuentra el local
