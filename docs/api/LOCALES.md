# Locales

## Obtener todos los locales
- **Método**: `GET`
- **Ruta**: `/api/locales`
- **Descripción**: Obtiene un listado de todos los locales registrados.
- **Parámetros de consulta**:
  - `plaza_id` (opcional): Filtrar locales por ID de plaza
  - `estado` (opcional): Filtrar por estado (activo/inactivo)
  - `tipo_comercio` (opcional): Filtrar por tipo de comercio
  - `id_gerente` (opcional): Filtrar por ID de gerente asignado
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
      "tipo_comercio": "restaurante",
      "estado": "activo",
      "plaza_id": 1,
      "id_gerente": null
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
      "tipo_comercio": "restaurante",
      "estado": "activo",
      "plaza_id": 1,
      "id_gerente": null
    }
    ```
  - 404 Not Found: Si no se encuentra el local

## Tipos de Comercio
Los locales pueden ser de los siguientes tipos:
- `restaurante` - Restaurantes y establecimientos de comida
- `cafeteria` - Cafeterías y establecimientos de café
- `tienda` - Tiendas de venta de productos
- `servicio` - Servicios varios
- `otro` - Otro tipo de comercio (valor por defecto)

## Campos del Modelo

### tipo_comercio (string, requerido)
- Tipo de comercio del local
- Valores permitidos: `restaurante`, `cafeteria`, `tienda`, `servicio`, `otro`
- Valor por defecto: `otro`
- Se convierte automáticamente a minúsculas

### id_gerente (integer, opcional)
- ID del usuario con rol 'gerente' asignado al local
- Debe ser un ID de usuario existente con rol 'gerente'
- Si se proporciona, el usuario debe existir y tener el rol 'gerente'
- Puede ser nulo si el local no tiene gerente asignado

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
    "tipo_comercio": "restaurante",
    "estado": "activo",
    "plaza_id": 1,
    "id_gerente": null
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
      "tipo_comercio": "restaurante",
      "estado": "activo",
      "plaza_id": 1,
      "id_gerente": null
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
    "tipo_comercio": "restaurante",
    "estado": "activo",
    "plaza_id": 2,
    "id_gerente": 1
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
