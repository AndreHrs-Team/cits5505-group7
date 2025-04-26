# User Data Structure
| Field|Type| Rule |
|------|----|------|
id	|INTEGER |	Primary key, auto-increment
name	|TEXT |	Not null
email	|TEXT |	Unique, not null
password	|TEXT |	Hashed by backend, not plaintext
role	|TEXT |	DEFAULT user (Value either 'user' or 'admin')
created_at	|INTEGER | DEFAULT (strftime('%s', 'now'))
updated_at	|INTEGER | DEFAULT (strftime('%s', 'now'))
deleted_at	|INTEGER |	Optional for soft-deletes (nullable)

# User API Contract
**Base URL:** `/api/v1/users`

## Endpoints

### GET `/api/v1/users`
Retrieve all users.

**Response 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "message": "Users retrieved successfully"
}
```

---

### GET `/api/v1/users/{id}`
Retrieve a single user by ID.

**Response 200 OK**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "message": "User retrieved successfully"
}
```

**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "User not found",
  "error": "USER_NOT_FOUND"
}
```

---

### POST `/api/v1/users`
Create a new user.

**Request Body**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response 201 Created**
```json
{
  "success": true,
  "data": {
    "id": 3,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "message": "User created successfully"
}
```

**Response 400 Bad Request (Validation Error)**
```json
{
  "success": false,
  "data": {
    "email": "Email is invalid or already taken",
    "password": "Password must be at least 8 characters"
  },
  "message": "Please correct the highlighted fields",
  "error": "VALIDATION_ERROR"
}
```

---

### PUT `/api/v1/users/{id}`
Update a user’s information.

**Request Body**
```json
{
  "name": "Updated Name",
  "email": "updated@example.com"
}
```

**Response 200 OK**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Updated Name",
    "email": "updated@example.com"
  },
  "message": "User updated successfully"
}
```

**Response 400 Bad Request (Validation Error)**
```json
{
  "success": false,
  "data": {
    "email": "Email format is invalid"
  },
  "message": "Please correct the highlighted fields",
  "error": "VALIDATION_ERROR"
}
```

**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "User not found",
  "error": "USER_NOT_FOUND"
}
```

---

### DELETE `/api/v1/users/{id}`
Delete a user by ID.

**Response 200 OK**
```json
{
  "success": true,
  "data": {},
  "message": "User deleted successfully"
}
```

**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "User not found",
  "error": "USER_NOT_FOUND"
}
```

## Validation Rules

| Field| Rule  |
|------|-------|
| name | Required, string, max 255 chars |
| email | Required, valid email, unique |
| password | Required (on create), min 8 chars |

