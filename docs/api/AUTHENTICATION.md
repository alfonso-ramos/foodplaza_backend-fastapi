# Authentication

This document describes the authentication process for the FoodPlaza API.

## Login

- **Method**: `POST`
- **Path**: `/api/v1/auth/login`
- **Description**: Authenticates a user with their email and password.

### Request Body

The request body must be a form with the following fields:

- `username` (string, required): The user's email address.
- `password` (string, required): The user's password.

### Responses

- **200 OK**: If the login is successful.

  ```json
  {
    "message": "Login successful"
  }
  ```

- **401 Unauthorized**: If the email or password are incorrect.

  ```json
  {
    "detail": "Incorrect username or password"
  }
  ```