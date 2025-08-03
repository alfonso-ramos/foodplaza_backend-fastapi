# Gestión de Pedidos

Este documento describe los endpoints disponibles para la gestión de pedidos en el sistema FoodPlaza.

## Estructura de Datos

### Pedido
```json
{
  "id": 1,
  "id_usuario": 1,
  "id_local": 1,
  "fecha_pedido": "2025-08-02T19:30:00",
  "estado_pedido": "pendiente",
  "total_pedido": 240.00,
  "instrucciones_especiales": "Sin cebolla",
  "tiempo_preparacion_estimado": 40,
  "items": [
    {
      "id": 1,
      "id_producto": 5,
      "cantidad": 2,
      "precio_unitario": 120.00,
      "instrucciones_especiales": "Bien cocido"
    }
  ]
}
```

### Estados de un Pedido
- `pendiente`: Recién creado
- `en_preparacion`: En proceso de preparación
- `listo_para_recoger`: Listo para ser recogido
- `completado`: Entregado al cliente
- `cancelado`: Cancelado por el restaurante o el cliente

## Endpoints

### 1. Crear un Pedido
Crea un nuevo pedido en el sistema.

**URL**: `POST /api/pedidos/`

**Body**:
```json
{
  "id_local": 1,
  "instrucciones_especiales": "Sin cebolla",
  "items": [
    {
      "id_producto": 5,
      "cantidad": 2,
      "precio_unitario": 120.00,
      "instrucciones_especiales": "Bien cocido"
    }
  ]
}
```

**Respuesta Exitosa (201)**:
```json
{
  "id": 1,
  "id_usuario": 1,
  "id_local": 1,
  "fecha_pedido": "2025-08-02T19:30:00",
  "estado_pedido": "pendiente",
  "total_pedido": 240.00,
  "instrucciones_especiales": "Sin cebolla",
  "tiempo_preparacion_estimado": 40,
  "items": [
    {
      "id": 1,
      "id_producto": 5,
      "cantidad": 2,
      "precio_unitario": 120.00,
      "instrucciones_especiales": "Bien cocido"
    }
  ]
}
```

### 2. Obtener un Pedido por ID
Obtiene los detalles de un pedido específico.

**URL**: `GET /api/pedidos/{pedido_id}`

**Respuesta Exitosa (200)**:
```json
{
  "id": 1,
  "id_usuario": 1,
  "id_local": 1,
  "fecha_pedido": "2025-08-02T19:30:00",
  "estado_pedido": "pendiente",
  "total_pedido": 240.00,
  "instrucciones_especiales": "Sin cebolla",
  "tiempo_preparacion_estimado": 40,
  "items": [
    {
      "id": 1,
      "id_producto": 5,
      "cantidad": 2,
      "precio_unitario": 120.00,
      "instrucciones_especiales": "Bien cocido"
    }
  ]
}
```

### 3. Actualizar Estado de un Pedido
Actualiza el estado de un pedido existente.

**URL**: `PATCH /api/pedidos/{pedido_id}`

**Body**:
```json
{
  "estado_pedido": "en_preparacion"
}
```

**Respuesta Exitosa (200)**:
```json
{
  "id": 1,
  "estado_pedido": "en_preparacion",
  "mensaje": "Estado del pedido actualizado correctamente"
}
```

### 4. Listar Pedidos de un Usuario
Obtiene todos los pedidos de un usuario específico.

**URL**: `GET /api/pedidos/usuario/{usuario_id}`

**Parámetros de Consulta**:
- `estado`: Filtrar por estado del pedido (opcional)
- `skip`: Número de registros a omitir (paginación)
- `limit`: Número máximo de registros a devolver (paginación)

**Respuesta Exitosa (200)**:
```json
[
  {
    "id": 1,
    "id_usuario": 1,
    "id_local": 1,
    "fecha_pedido": "2025-08-02T19:30:00",
    "estado_pedido": "pendiente",
    "total_pedido": 240.00,
    "tiempo_preparacion_estimado": 40
  },
  {
    "id": 2,
    "id_usuario": 1,
    "id_local": 2,
    "fecha_pedido": "2025-08-01T14:20:00",
    "estado_pedido": "completado",
    "total_pedido": 180.50,
    "tiempo_preparacion_estimado": 30
  }
]
```

### 5. Listar Pedidos de un Local
Obtiene todos los pedidos de un local específico.

**URL**: `GET /api/pedidos/local/{local_id}`

**Parámetros de Consulta**:
- `estado`: Filtrar por estado del pedido (opcional)
- `skip`: Número de registros a omitir (paginación)
- `limit`: Número máximo de registros a devolver (paginación)

**Respuesta Exitosa (200)**:
```json
[
  {
    "id": 1,
    "id_usuario": 1,
    "usuario_nombre": "Juan Pérez",
    "fecha_pedido": "2025-08-02T19:30:00",
    "estado_pedido": "pendiente",
    "total_pedido": 240.00,
    "tiempo_preparacion_estimado": 40
  },
  {
    "id": 3,
    "id_usuario": 2,
    "usuario_nombre": "María García",
    "fecha_pedido": "2025-08-02T18:15:00",
    "estado_pedido": "en_preparacion",
    "total_pedido": 320.75,
    "tiempo_preparacion_estimado": 45
  }
]
```

## Consideraciones de Seguridad

- Los usuarios solo pueden ver sus propios pedidos
- Los administradores pueden ver todos los pedidos
- Los gerentes pueden ver los pedidos de sus locales asignados
- Solo los administradores y gerentes pueden actualizar el estado de los pedidos
