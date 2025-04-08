## General Responses
All responses follow this structure:

```json
{
  "success": true,
  "data": { },
  "message": "A readable message for the user",
  "error": "OPTIONAL_ERROR_CODE"
}
```

## General Errors
### 401 Unauthorized
```json
{
  "success": false,
  "data": {},
  "message": "You must be logged in to perform this action",
  "error": "UNAUTHORIZED"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "data": {},
  "message": "You do not have permission to access this resource",
  "error": "FORBIDDEN"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "data": {},
  "message": "An unexpected error occurred. Please try again later",
  "error": "INTERNAL_SERVER_ERROR"
}
```


## Notes
- `error` is optional and used for frontend error code handling.
- `message` should always provide user-readable info.
