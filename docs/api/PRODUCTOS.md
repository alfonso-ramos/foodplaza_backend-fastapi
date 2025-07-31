# Products

This document describes the endpoints for managing products.

## Get all products for a menu

- **Method**: `GET`
- **Path**: `/api/v1/productos/menu/{menu_id}`
- **Description**: Gets a list of all products for a specific menu.

### Responses

- **200 OK**: Returns a list of products.

## Get a product by ID

- **Method**: `GET`
- **Path**: `/api/v1/productos/{producto_id}`
- **Description**: Gets a single product by its ID.

### Responses

- **200 OK**: Returns the product's data.
- **404 Not Found**: If the product is not found.

## Create a new product

- **Method**: `POST`
- **Path**: `/api/v1/productos/`
- **Description**: Creates a new product.

### Request Body

```json
{
  "nombre": "string",
  "descripcion": "string",
  "precio": 0,
  "disponible": true,
  "categoria": "string",
  "id_menu": 0
}
```

### Responses

- **201 Created**: If the product is created successfully.

## Update a product

- **Method**: `PUT`
- **Path**: `/api/v1/productos/{producto_id}`
- **Description**: Updates an existing product's data.

### Request Body

```json
{
  "nombre": "string",
  "descripcion": "string",
  "precio": 0,
  "disponible": true,
  "categoria": "string",
  "id_menu": 0
}
```

### Responses

- **200 OK**: Returns the updated product's data.
- **404 Not Found**: If the product is not found.

## Delete a product

- **Method**: `DELETE`
- **Path**: `/api/v1/productos/{producto_id}`
- **Description**: Deletes a product by its ID.

### Responses

- **204 No Content**: If the product is deleted successfully.
- **404 Not Found**: If the product is not found.