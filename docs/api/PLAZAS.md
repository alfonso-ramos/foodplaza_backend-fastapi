# Plazas

This document describes the endpoints for managing plazas.

## Get all plazas

- **Method**: `GET`
- **Path**: `/api/v1/plazas/`
- **Description**: Gets a list of all plazas.

### Responses

- **200 OK**: Returns a list of plazas.

## Get a plaza by ID

- **Method**: `GET`
- **Path**: `/api/v1/plazas/{plaza_id}`
- **Description**: Gets a single plaza by its ID.

### Responses

- **200 OK**: Returns the plaza's data.
- **404 Not Found**: If the plaza is not found.

## Create a new plaza

- **Method**: `POST`
- **Path**: `/api/v1/plazas/`
- **Description**: Creates a new plaza.

### Request Body

```json
{
  "nombre": "string",
  "direccion": "string",
  "estado": "activo"
}
```

### Responses

- **201 Created**: If the plaza is created successfully.

## Update a plaza

- **Method**: `PUT`
- **Path**: `/api/v1/plazas/{plaza_id}`
- **Description**: Updates an existing plaza's data.

### Request Body

```json
{
  "nombre": "string",
  "direccion": "string",
  "estado": "activo"
}
```

### Responses

- **200 OK**: Returns the updated plaza's data.
- **404 Not Found**: If the plaza is not found.

## Delete a plaza

- **Method**: `DELETE`
- **Path**: `/api/v1/plazas/{plaza_id}`
- **Description**: Deletes a plaza by its ID.

### Responses

- **204 No Content**: If the plaza is deleted successfully.
- **404 Not Found**: If the plaza is not found.