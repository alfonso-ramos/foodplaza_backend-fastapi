# Images

This document describes the endpoints for managing images.

## Upload a new image for an entity

- **Method**: `POST`
- **Path**: `/api/v1/imagenes/upload/{tipo_entidad}/{entidad_id}`
- **Description**: Uploads a new image for a specific entity (plaza, local, product, or user).

### Path Parameters

- `tipo_entidad` (string, required): The type of entity (plaza, local, product, or user).
- `entidad_id` (integer, required): The ID of the entity.

### Request Body

The request body must be a form with the following fields:

- `file` (file, required): The image file to upload.
- `es_principal` (boolean, optional): Whether the image should be the main one for the entity.
- `orden` (integer, optional): The display order of the image.

### Responses

- **201 Created**: If the image is uploaded successfully.
- **400 Bad Request**: If the entity type is invalid.
- **500 Internal Server Error**: If there is an error processing the image.

## Get all images for an entity

- **Method**: `GET`
- **Path**: `/api/v1/imagenes/{tipo_entidad}/{entidad_id}`
- **Description**: Gets all images associated with a specific entity.

### Responses

- **200 OK**: Returns a list of images.
- **400 Bad Request**: If the entity type is invalid.

## Get the main image for an entity

- **Method**: `GET`
- **Path**: `/api/v1/imagenes/{tipo_entidad}/{entidad_id}/principal`
- **Description**: Gets the main image for a specific entity.

### Responses

- **200 OK**: Returns the main image's data.
- **400 Bad Request**: If the entity type is invalid.
- **404 Not Found**: If no main image is found for the entity.

## Update image metadata

- **Method**: `PUT`
- **Path**: `/api/v1/imagenes/{imagen_id}`
- **Description**: Updates the metadata of an existing image.

### Request Body

```json
{
  "es_principal": true,
  "orden": 0,
  "metadata": {}
}
```

### Responses

- **200 OK**: Returns the updated image's data.
- **404 Not Found**: If the image is not found.

## Delete an image

- **Method**: `DELETE`
- **Path**: `/api/v1/imagenes/{imagen_id}`
- **Description**: Deletes an image by its ID.

### Responses

- **204 No Content**: If the image is deleted successfully.
- **404 Not Found**: If the image is not found.