# Locales

## Obtener todos los locales
- **Método**: `GET`
- **Ruta**: `/api/locales`
- **Descripción**: Obtiene un listado de todos los locales registrados.
- **Parámetros de consulta**:
  - `plazaId` (opcional): Filtrar locales por ID de plaza
  - `estado` (opcional): Filtrar por estado (activo/inactivo)
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Local 1",
      "descripcion": "Descripción del local",
      "direccion": "Dirección del local",
      "horarioApertura": "09:00",
      "horarioCierre": "22:00",
      "estado": "activo",
      "idPlaza": 1
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
      "horarioApertura": "09:00",
      "horarioCierre": "22:00",
      "estado": "activo",
      "idPlaza": 1
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
    "horarioApertura": "09:00",
    "horarioCierre": "22:00",
    "estado": "activo",
    "idPlaza": 1
  }
  ```
- **Respuestas**:
  - 201 Created: Devuelve el local creado
  - 400 Bad Request: Si los datos son inválidos
  - 404 Not Found: Si la plaza especificada no existe

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
    "horarioApertura": "10:00",
    "horarioCierre": "23:00",
    "estado": "activo",
    "idPlaza": 2
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
