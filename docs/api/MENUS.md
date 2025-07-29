# Menús

## Crear un nuevo menú
- **Método**: `POST`
- **Ruta**: `/api/menus`
- **Descripción**: Crea un nuevo menú en el sistema.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "id_local": 1,
    "nombre_menu": "Menú de Prueba",
    "descripcion": "Descripción del menú de prueba"
  }
  ```
- **Respuestas**:
  - 201 Created: Menú creado exitosamente
    ```json
    {
      "id": 1,
      "id_local": 1,
      "nombre_menu": "Menú de Prueba",
      "descripcion": "Descripción del menú de prueba"
    }
    ```
  - 400 Bad Request: Datos inválidos o faltantes
  - 404 Not Found: Si el local no existe

## Obtener menú por ID
- **Método**: `GET`
- **Ruta**: `/api/menus/{menu_id}`
- **Parámetros de ruta**:
  - `menu_id` (requerido): ID del menú a buscar
- **Respuestas**:
  - 200 OK: Devuelve el menú solicitado
    ```json
    {
      "id": 1,
      "id_local": 1,
      "nombre_menu": "Menú de Prueba",
      "descripcion": "Descripción del menú de prueba"
    }
    ```
  - 404 Not Found: Si el menú no existe

## Obtener menús por local
- **Método**: `GET`
- **Ruta**: `/api/menus/local/{local_id}`
- **Parámetros de ruta**:
  - `local_id` (requerido): ID del local cuyos menús se quieren obtener
- **Parámetros de consulta**:
  - `skip` (opcional, default: 0): Número de registros a saltar
  - `limit` (opcional, default: 100): Número máximo de registros a devolver
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "id_local": 1,
      "nombre_menu": "Menú de Prueba",
      "descripcion": "Descripción del menú de prueba"
    }
  ]
  ```
  - 404 Not Found: Si el local no existe

## Actualizar un menú
- **Método**: `PUT`
- **Ruta**: `/api/menus/{menu_id}`
- **Parámetros de ruta**:
  - `menu_id` (requerido): ID del menú a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "id_local": 1,
    "nombre_menu": "Menú Actualizado",
    "descripcion": "Nueva descripción"
  }
  ```
  > **Nota**: Todos los campos son opcionales. Solo se actualizarán los campos proporcionados.
- **Respuestas**:
  - 200 OK: Menú actualizado exitosamente
    ```json
    {
      "id": 1,
      "id_local": 1,
      "nombre_menu": "Menú Actualizado",
      "descripcion": "Nueva descripción"
    }
    ```
  - 400 Bad Request: Datos inválidos
  - 404 Not Found: Si el menú no existe

## Eliminar un menú
- **Método**: `DELETE`
- **Ruta**: `/api/menus/{menu_id}`
- **Parámetros de ruta**:
  - `menu_id` (requerido): ID del menú a eliminar
- **Respuestas**:
  - 204 No Content: Menú eliminado exitosamente
  - 404 Not Found: Si el menú no existe
