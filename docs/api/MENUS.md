# Menus

This document describes the endpoints for managing menus.

## Get all menus for a locale

- **Method**: `GET`
- **Path**: `/api/v1/menus/local/{local_id}`
- **Description**: Gets a list of all menus for a specific locale.

### Responses

- **200 OK**: Returns a list of menus.

## Get a menu by ID

- **Method**: `GET`
- **Path**: `/api/v1/menus/{menu_id}`
- **Description**: Gets a single menu by its ID.

### Responses

- **200 OK**: Returns the menu's data.
- **404 Not Found**: If the menu is not found.

## Create a new menu

- **Method**: `POST`
- **Path**: `/api/v1/menus/`
- **Description**: Creates a new menu.

### Request Body

```json
{
  "nombre_menu": "string",
  "descripcion": "string",
  "id_local": 0
}
```

### Responses

- **201 Created**: If the menu is created successfully.

## Update a menu

- **Method**: `PUT`
- **Path**: `/api/v1/menus/{menu_id}`
- **Description**: Updates an existing menu's data.

### Request Body

```json
{
  "nombre_menu": "string",
  "descripcion": "string",
  "id_local": 0
}
```

### Responses

- **200 OK**: Returns the updated menu's data.
- **404 Not Found**: If the menu is not found.

## Delete a menu

- **Method**: `DELETE`
- **Path**: `/api/v1/menus/{menu_id}`
- **Description**: Deletes a menu by its ID.

### Responses

- **204 No Content**: If the menu is deleted successfully.
- **404 Not Found**: If the menu is not found.