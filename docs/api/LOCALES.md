# Locales

This document describes the endpoints for managing locales.

## Get all locales

- **Method**: `GET`
- **Path**: `/api/v1/locales/`
- **Description**: Gets a list of all locales.

### Responses

- **200 OK**: Returns a list of locales.

## Get a locale by ID

- **Method**: `GET`
- **Path**: `/api/v1/locales/{locale_id}`
- **Description**: Gets a single locale by its ID.

### Responses

- **200 OK**: Returns the locale's data.
- **404 Not Found**: If the locale is not found.

## Create a new locale

- **Method**: `POST`
- **Path**: `/api/v1/locales/`
- **Description**: Creates a new locale.

### Request Body

```json
{
  "nombre": "string",
  "descripcion": "string",
  "direccion": "string",
  "horario_apertura": "string",
  "horario_cierre": "string",
  "tipo_comercio": "restaurante",
  "estado": "activo",
  "plaza_id": 0,
  "id_gerente": 0
}
```

### Responses

- **201 Created**: If the locale is created successfully.

## Update a locale

- **Method**: `PUT`
- **Path**: `/api/v1/locales/{locale_id}`
- **Description**: Updates an existing locale's data.

### Request Body

```json
{
  "nombre": "string",
  "descripcion": "string",
  "direccion": "string",
  "horario_apertura": "string",
  "horario_cierre": "string",
  "tipo_comercio": "restaurante",
  "estado": "activo",
  "plaza_id": 0,
  "id_gerente": 0
}
```

### Responses

- **200 OK**: Returns the updated locale's data.
- **404 Not Found**: If the locale is not found.

## Delete a locale

- **Method**: `DELETE`
- **Path**: `/api/v1/locales/{locale_id}`
- **Description**: Deletes a locale by its ID.

### Responses

- **204 No Content**: If the locale is deleted successfully.
- **404 Not Found**: If the locale is not found.