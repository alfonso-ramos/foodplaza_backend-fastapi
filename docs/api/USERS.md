# Usuarios

## Obtener todos los usuarios
- **Método**: `GET`
- **Ruta**: `/api/usuarios`
- **Descripción**: Obtiene un listado de todos los usuarios registrados.
- **Respuesta exitosa (200 OK)**: 
  ```json
  [
    {
      "id": 1,
      "nombre": "juan123",
      "email": "usuario1@ejemplo.com",
      "telefono": "1234567890",
      "fechaRegistro": "2025-07-26T10:00:00"
    },
    {
      "id": 2,
      "nombre": "maria456",
      "email": "usuario2@ejemplo.com",
      "telefono": "0987654321",
      "fechaRegistro": "2025-07-25T09:15:00"
    }
  ]
  ```

## Obtener usuario por ID
- **Método**: `GET`
- **Ruta**: `/api/usuarios/{id}`
- **Parámetros de rta**:
  - `id` (requerido): ID del usuario a buscar
- **Respuestas**:
  - 200 OK: Devuelve los detalles del usuario
    ```json
    {
      "id": 1,
      "nombre": "juan123",
      "email": "usuario@ejemplo.com",
      "telefono": "1234567890",
      "fechaRegistro": "2025-07-26T10:00:00"
    }
    ```
  - 404 Not Found: Usuario no encontrado

## Actualizar usuario
- **Método**: `PUT`
- **Ruta**: `/api/usuarios/{id}`
- **Parámetros de rta**:
  - `id` (requerido): ID del usuario a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "nuevoUsuario",
    "email": "nuevo@ejemplo.com",
    "telefono": "0987654321",
    "password": "nuevaContraseña123"
  }
  ```
- **Campos actualizables**:
  - `nombre`: Nuevo nombre de usuario (debe ser único)
  - `email`: Nuevo correo electrónico (debe ser único y tener formato válido)
  - `telefono`: Nuevo número de teléfono (10 dígitos)
  - `password`: Nueva contraseña (mínimo 6 caracteres)
- **Respuestas**:
  - 200 OK: Usuario actualizado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "nuevoUsuario",
      "email": "nuevo@ejemplo.com",
      "telefono": "0987654321",
      "fechaRegistro": "2025-07-26T10:00:00"
    }
    ```
  - 400 Bad Request: Datos inválidos o faltantes
  - 404 Not Found: Usuario no encontrado
  - 409 Conflict: El nombre de usuario o correo electrónico ya está en uso

## Eliminar usuario
- **Método**: `DELETE`
- **Ruta**: `/api/usuarios/{id}`
- **Parámetros de rta**:
  - `id` (requerido): ID del usuario a eliminar
- **Respuestas**:
  - 204 No Content: Usuario eliminado correctamente
  - 404 Not Found: Usuario no encontrado
