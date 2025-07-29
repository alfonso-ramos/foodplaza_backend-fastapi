# Usuarios

## Crear un nuevo usuario
- **Método**: `POST`
- **Ruta**: `/api/usuarios`
- **Descripción**: Crea un nuevo usuario con rol 'usuario' por defecto.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "telefono": "+521234567890",
    "password": "Contraseña123"
  }
  ```
- **Validaciones**:
  - `nombre`: obligatorio, máximo 100 caracteres
  - `email`: obligatorio, formato válido y único
  - `password`: mínimo 8 caracteres
  - `telefono`: opcional, máximo 20 caracteres
- **Respuestas**:
  - 201 Created: Usuario creado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "email": "juan@ejemplo.com",
      "telefono": "+521234567890",
      "rol": "usuario",
      "estado": "activo",
      "fecha_creacion": "2025-07-28T12:00:00",
      "fecha_actualizacion": "2025-07-28T12:00:00"
    }
    ```
  - 400 Bad Request: Datos inválidos o email ya registrado

## Iniciar sesión
- **Método**: `POST`
- **Ruta**: `/api/usuarios/login`
- **Descripción**: Autentica a un usuario con email y contraseña.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "email": "juan@ejemplo.com",
    "password": "Contraseña123"
  }
  ```
- **Respuestas**:
  - 200 OK: Inicio de sesión exitoso
    ```json
    {
      "mensaje": "Inicio de sesión exitoso",
      "usuario_id": 1,
      "nombre": "Juan Pérez",
      "rol": "usuario"
    }
    ```
  - 401 Unauthorized: Credenciales incorrectas

## Obtener todos los usuarios
- **Método**: `GET`
- **Ruta**: `/api/usuarios`
- **Descripción**: Obtiene un listado paginado de usuarios.
- **Parámetros de consulta**:
  - `skip` (opcional, default: 0): Número de registros a saltar
  - `limit` (opcional, default: 100): Número máximo de registros a devolver
  - `estado` (opcional): Filtrar por estado ('activo' o 'inactivo')
- **Respuesta exitosa (200 OK)**: 
  ```json
  [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "email": "juan@ejemplo.com",
      "telefono": "+521234567890",
      "rol": "usuario",
      "estado": "activo",
      "fecha_creacion": "2025-07-28T12:00:00",
      "fecha_actualizacion": "2025-07-28T12:00:00"
    }
  ]
  ```
  - 400 Bad Request: Parámetros de consulta inválidos

## Obtener usuario por ID
- **Método**: `GET`
- **Ruta**: `/api/usuarios/{usuario_id}`
- **Parámetros de ruta**:
  - `usuario_id` (requerido): ID del usuario a buscar
- **Respuestas**:
  - 200 OK: Devuelve los detalles del usuario
    ```json
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "email": "juan@ejemplo.com",
      "telefono": "+521234567890",
      "rol": "usuario",
      "estado": "activo",
      "fecha_creacion": "2025-07-28T12:00:00",
      "fecha_actualizacion": "2025-07-28T12:00:00"
    }
    ```
  - 404 Not Found: Usuario no encontrado

## Actualizar usuario
- **Método**: `PUT`
- **Ruta**: `/api/usuarios/{usuario_id}`
- **Parámetros de ruta**:
  - `usuario_id` (requerido): ID del usuario a actualizar
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "Juan Pérez Actualizado",
    "email": "nuevo@ejemplo.com",
    "telefono": "+521234567890",
    "password": "nuevaContraseña123",
    "rol": "usuario",
    "estado": "activo"
  }
  ```
- **Campos actualizables**:
  - `nombre` (opcional): Nuevo nombre
  - `email` (opcional): Nuevo correo electrónico (debe ser único)
  - `telefono` (opcional): Nuevo número de teléfono
  - `password` (opcional): Nueva contraseña (mínimo 8 caracteres)
  - `rol` (opcional): Nuevo rol ('usuario', 'gerente', 'administrador')
  - `estado` (opcional): Nuevo estado ('activo', 'inactivo')
- **Respuestas**:
  - 200 OK: Usuario actualizado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "Juan Pérez Actualizado",
      "email": "nuevo@ejemplo.com",
      "telefono": "+521234567890",
      "rol": "usuario",
      "estado": "activo",
      "fecha_creacion": "2025-07-28T12:00:00",
      "fecha_actualizacion": "2025-07-28T13:00:00"
    }
    ```
  - 400 Bad Request: Datos inválidos
  - 404 Not Found: Usuario no encontrado
  - 409 Conflict: El correo electrónico ya está en uso

## Eliminar usuario
- **Método**: `DELETE`
- **Ruta**: `/api/usuarios/{usuario_id}`
- **Descripción**: Marca un usuario como inactivo (eliminación lógica)
- **Parámetros de ruta**:
  - `usuario_id` (requerido): ID del usuario a marcar como inactivo
- **Respuestas**:
  - 204 No Content: Usuario marcado como inactivo correctamente
  - 404 Not Found: Usuario no encontrado
