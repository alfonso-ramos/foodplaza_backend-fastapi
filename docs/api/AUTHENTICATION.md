# Autenticación

## Registrar un nuevo usuario
- **Método**: `POST`
- **Ruta**: `/api/auth/registro`
- **Descripción**: Registra un nuevo usuario en el sistema.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre": "juan123",
    "password": "contraseña123",
    "email": "usuario@ejemplo.com",
    "telefono": "1234567890"
  }
  ```
- **Validaciones**:
  - Nombre: obligatorio, máximo 100 caracteres
  - Contraseña: obligatoria, mínimo 6 caracteres
  - Email: obligatorio, debe tener formato de email válido
  - Teléfono: obligatorio, exactamente 10 dígitos

- **Respuestas**:
  - 201 Created: Usuario registrado exitosamente
    ```json
    {
      "id": 1,
      "nombre": "juan123",
      "email": "usuario@ejemplo.com",
      "telefono": "1234567890",
      "fechaRegistro": "2025-07-27T02:03:56.12345"
    }
    ```
  - 400 Bad Request: Datos inválidos o faltantes
  - 409 Conflict: El nombre de usuario o correo electrónico ya está en uso
