# Users

This document describes the endpoints for managing users.

## Create a new user

- **Method**: `POST`
- **Path**: `/api/v1/usuarios/`
- **Description**: Creates a new user.

### Request Body

```json
{
  "email": "user@example.com",
  "nombre": "string",
  "apellido": "string",
  "password": "string",
  "tipo": "cliente",
  "estado": "activo"
}
```

### Responses

- **201 Created**: If the user is created successfully.
- **400 Bad Request**: If a user with the same email already exists.

## Get all users

- **Method**: `GET`
- **Path**: `/api/v1/usuarios/`
- **Description**: Gets a list of all users.

### Responses

- **200 OK**: Returns a list of users.

## Get a user by ID

- **Method**: `GET`
- **Path**: `/api/v1/usuarios/{usuario_id}`
- **Description**: Gets a single user by their ID.

### Responses

- **200 OK**: Returns the user's data.
- **404 Not Found**: If the user is not found.

## Update a user

- **Method**: `PUT`
- **Path**: `/api/v1/usuarios/{usuario_id}`
- **Description**: Updates an existing user's data.

### Request Body

```json
{
  "email": "user@example.com",
  "nombre": "string",
  "apellido": "string",
  "password": "string",
  "tipo": "cliente",
  "estado": "activo"
}
```

### Responses

- **200 OK**: Returns the updated user's data.
- **404 Not Found**: If the user is not found.

## Delete a user

- **Method**: `DELETE`
- **Path**: `/api/v1/usuarios/{usuario_id}`
- **Description**: Deletes a user by their ID.

### Responses

- **204 No Content**: If the user is deleted successfully.
- **404 Not Found**: If the user is not found.