# User Data Structure

## Tables

### 1. users

This table stores user account information and preferences.

| Field Name            | Type         | Description                                                  |
| --------------------- | ------------ | ------------------------------------------------------------ |
| `id`                  | INTEGER      | Primary key, auto-incremented, unique identifier for each user. |
| `username`            | VARCHAR(64)  | User's chosen username, must be unique.                      |
| `email`               | VARCHAR(120) | User's email address, must be unique.                        |
| `password_hash`       | VARCHAR(128) | Hashed password for secure authentication.                   |
| `created_at`          | DATETIME     | Timestamp when the user account was created.                 |
| `last_login`          | DATETIME     | Timestamp of the user's last login.                          |
| `is_active`           | BOOLEAN      | Indicates if the user account is active or deactivated.      |
| `is_admin`            | BOOLEAN      | Indicates if the user has admin privileges.                  |
| `updated_at`          | DATETIME     | Timestamp when the user account was last updated.            |
| `first_name`          | VARCHAR(64)  | User's first name.                                           |
| `last_name`           | VARCHAR(64)  | User's last name.                                            |
| `gender`              | VARCHAR(20)  | User's gender.                                               |
| `birth_date`          | DATE         | User's birth date.                                           |
| `height`              | FLOAT        | User's height (in cm).                                       |
| `weight`              | FLOAT        | User's weight (in kg).                                       |
| `default_share_privacy` | VARCHAR(20) | Default privacy level for sharing: 'complete', 'overview', or 'achievements'. |
| `default_share_modules` | TEXT        | JSON array of modules to share by default.                   |
| `default_share_template` | VARCHAR(20) | Default template for sharing: 'medical' or 'social'.        |
| `default_share_expiry` | INTEGER      | Default expiry time in days for share links.                 |

------

# User API Contract

## 1. Authentication

### POST `/auth/register`

Register a new user.

**Request Body (JSON):**

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**

- `201 Created` on success
- `400 Bad Request` if validation fails

**Example Response:**

```json
{
  "success": true,
  "message": "Registration successful"
}
```

------

### POST `/auth/login`

Authenticate and receive a token.

**Request Body (JSON):**

```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**

- `200 OK` on success
- `401 Unauthorized` if credentials are invalid

**Example Response:**

```json
{
  "success": true,
  "message": "Login successful",
  "token": "jwt-token-here"
}
```

------

### POST `/auth/logout`

Log out the current user (invalidate token).

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

------

### POST `/auth/reset_password_request`

Request a password reset.

**Request Body (JSON):**

```json
{
  "email": "string"
}
```

**Response:**

- `200 OK` on success (regardless of whether email exists)

**Example Response:**

```json
{
  "success": true,
  "message": "Password reset instructions sent to email if it exists"
}
```

------

### POST `/auth/reset_password/<token>`

Reset password using a valid token.

**Request Body (JSON):**

```json
{
  "password": "string",
  "confirm_password": "string"
}
```

**Response:**

- `200 OK` on success
- `400 Bad Request` if passwords don't match
- `401 Unauthorized` if token is invalid

**Example Response:**

```json
{
  "success": true,
  "message": "Password reset successful"
}
```

------
