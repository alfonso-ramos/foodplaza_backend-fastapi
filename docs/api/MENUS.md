# Menús

## Crear un nuevo menú
- **Método**: `POST`
- **Ruta**: `/api/menus`
- **Descripción**: Crea un nuevo menú en el sistema.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "idLocal": 1,
    "nombreMenu": "Menú de Prueba",
    "descripcion": "Descripción del menú de prueba"
  }
  ```
- **Respuestas**:
  - 201 Created: Menú creado exitosamente
    ```json
    {
      "id": 1,
      "idLocal": 1,
      "nombreMenu": "Menú de Prueba",
      "descripcion": "Descripción del menú de prueba"
    }
    ```
  - 400 Bad Request: Datos inválidos o faltantes
  - 404 Not Found: Si el local no existe

## Obtener todos los menús
- **Método**: `GET`
- **Ruta**: `/api/menus`
- **Descripción**: Obtiene un listado de todos los menús.
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "idLocal": 1,
      "nombreMenu": "Menú de Prueba",
      "descripcion": "Descripción del menú de prueba"
    }
  ]
  ```

## Obtener menú por ID
- **Método**: `GET`
- **Ruta**: `/api/menus/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del menú a buscar
- **Respuestas**:
  - 200 OK: Devuelve el menú solicitado
    ```json
    {
      "id": 1,
      "idLocal": 1,
      "nombreMenu": "Menú de Prueba",
      "descripcion": "Descripción del menú de prueba"
    }
    ```
  - 404 Not Found: Menú no encontrado

## Obtener menús por local
- **Método**: `GET`
- **Ruta**: `/api/menus/local/{idLocal}`
- **Parámetros de ruta**:
  - `idLocal` (requerido): ID del local
- **Respuestas**:
  - 200 OK: Lista de menús del local
    ```json
    [
      {
        "id": 1,
        "idLocal": 1,
        "nombreMenu": "Menú de Prueba",
        "descripcion": "Descripción del menú de prueba"
      }
    ]
    ```
  - 404 Not Found: Si el local no existe

## Actualizar un menú
- **Método**: `PUT`
- **Ruta**: `/api/menus/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del menú a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "idLocal": 1,
    "nombreMenu": "Menú Actualizado",
    "descripcion": "Nueva descripción del menú"
  }
  ```
- **Respuestas**:
  - 200 OK: Menú actualizado exitosamente
    ```json
    {
      "id": 1,
      "idLocal": 1,
      "nombreMenu": "Menú Actualizado",
      "descripcion": "Nueva descripción del menú"
    }
    ```
  - 400 Bad Request: Datos inválidos
  - 404 Not Found: Menú no encontrado

## Eliminar un menú
- **Método**: `DELETE`
- **Ruta**: `/api/menus/{id}`
- **Parámetros de ruta**:
  - `id` (requerido): ID del menú a eliminar
- **Respuestas**:
  - 200 OK: Menú eliminado exitosamente
    ```json
    {
      "success": true,
      "message": "Menú eliminado exitosamente"
    }
    ```
  - 404 Not Found: Menú no encontrado

## Buscar menús por nombre
- **Método**: `GET`
- **Ruta**: `/api/menus/buscar`
- **Parámetros de consulta**:
  - `nombre` (requerido): Texto para buscar en el nombre del menú
- **Respuesta exitosa (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "idLocal": 1,
      "nombreMenu": "Menú de Prueba",
      "descripcion": "Descripción del menú de prueba"
    }
  ]
  ```
