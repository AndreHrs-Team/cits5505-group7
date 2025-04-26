## 1. Table Definitions
------
## Categories
Field	| Type | 	Notes
------|------|---------
id	| INTEGER | 	Primary key, auto-increment
type |	TEXT |	EXPENSE or INCOME
name	| TEXT | 	E.g., "Groceries", "Fuel"
icon	| TEXT | 	Optional (for UI display), should have default value to placeholder
user_id	| INTEGER |  (nullable)	FK to finance(id) — null means global/shared category
created_at	| INTEGER | DEFAULT (strftime('%s', 'now'))	
updated_at	| INTEGER | DEFAULT (strftime('%s', 'now'))

## User-Accounts (e.g., Cash, Credit Card, Bank Account)
Field	| Type |	Notes
------|------|---------
id	| INTEGER |	Primary key, auto-increment
user_id	| INTEGER |	FK to finance(id)
name	| TEXT |	e.g., "Commbank", "Cash", "Mastercard"
type	| TEXT |	Optional, e.g., "bank", "wallet"
note | TEXT |	Optional, e.g., "bank", "wallet"
balance	| REAL |	Optional, e.g., "bank", "wallet"
created_at	| INTEGER |	DEFAULT (strftime('%s', 'now'))
updated_at	| INTEGER |	DEFAULT (strftime('%s', 'now'))

## Transaction
Field |	Type |	Rule / Note
------|------|---------------
id |	INTEGER |	Primary key, auto-increment
type|	TEXT |	EXPENSE or INCOME
user_id |	INTEGER |	FK to finance(id)
account_id |	INTEGER |	FK to accounts(id)
category_id |	INTEGER |	FK to categories(id)
amount |	REAL |	Amount in base currency
date |	INTEGER |	Epoch timestamp for analysis/plotting
title |	TEXT |	(nullable) Short description (e.g. "Groceries", "Rent")
note |	TEXT |	(nullable) Optional notes/details
created_at |	INTEGER |	DEFAULT (strftime('%s', 'now')) Epoch timestamp
updated_at |	INTEGER |	DEFAULT (strftime('%s', 'now')) Epoch timestamp

## 2. Finance API Contract
**Base URL:** `/api/v1/finance`

## Aggregation Endpoints
### GET `/api/v1/finance/aggregate/balance`
Get summed account balance for current balance overview

**Response 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "balance": 2450
    }
  ],
  "message": "balance data retrieved successfully"
}
```
---
### GET `/api/v1/finance/aggregate/categorical_monthly_graph`
Get time series data for ChartJs 

**Query Parameters**:
- start_date (string, optional): timestamp
- end_date (string, optional): timestamp.

**Response 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "xValues": ["categories", "categories"], // array of corresponding categories
      "yValues": [10, 20] // array of corresponding values
    }
  ],
  "message": "balance data retrieved successfully"
}
```
---
## CRUD Endpoints


### GET /api/v1/finance/categories
List all categories

**Query Parameters**:
- page (int, optional): page number, starting from 0, default 0.
- limit (int, optional): item per page, default 10.

**Response 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "type": "EXPENSE",
      "name": "Groceries",
      "icon": "placeholder",
      "user_id": 3,
      "created_at": 1618579200,
      "updated_at": 1618579200
    }
  ],
  "message": "Categories retrieved successfully"
}
```
---

### POST /api/v1/finance/categories
Create new category
**Request Body**
```json
{
  "type": "EXPENSE",
  "name": "Groceries",
  "icon": "placeholder",
  "user_id": 3
}
```
**Response 201 Created**
```json
{
  "success": true,
  "data": {
    "id": 1
  },
  "message": "Category created successfully"
}
```

**Response 400 Bad Request**
```json
{
  "success": false,
  "data": {
    "type": "Type is required",
    "name": "Name must not be empty"
  },
  "message": "Please correct the highlighted fields",
  "error": "VALIDATION_ERROR"
}
```
---

### PUT /api/v1/finance/categories/:id
// Update category
**Request Body**
```json
{
  "name": "Fuel"
}
```

**Response 200 OK**
```json
{
  "success": true,
  "data": {},
  "message": "Category updated successfully"
}
```

**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "Category not found",
  "error": "CATEGORY_NOT_FOUND"
}
```
---
### DELETE /api/v1/finance/categories/:id
**Response 200 OK**
```json
{
  "success": true,
  "data": {},
  "message": "Category deleted successfully"
}
```
---
**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "Category not found",
  "error": "CATEGORY_NOT_FOUND"
}
```
---
CRUD for Accounts

### GET /api/v1/finance/accounts
**Response 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Cash",
      "type": "wallet",
      "note": "Personal wallet",
      "balance": 100.0,
      "user_id": 3,
      "created_at": 1618579200,
      "updated_at": 1618579200
    }
  ],
  "message": "Accounts retrieved successfully"
}
```

**Response 401 Unauthorized**
```json
{
  "success": false,
  "data": {},
  "message": "You must be logged in to perform this action",
  "error": "UNAUTHORIZED"
}
```
---
### POST /api/v1/finance/accounts
**Request Body**
```json
{
  "name": "Cash",
  "type": "wallet",
  "note": "Personal wallet",
  "balance": 100.0,
  "user_id": 3
}
```

**Response 201 Created**
```json
{
  "success": true,
  "data": {
    "id": 1
  },
  "message": "Account created successfully"
}
```

**Response 400 Bad Request**
```json
{
  "success": false,
  "data": {
    "name": "Name is required"
  },
  "message": "Please correct the highlighted fields",
  "error": "VALIDATION_ERROR"
}
```
---
### PUT /api/v1/finance/accounts/:id
**Request Body**
```json
{
  "note": "Updated note"
}
```

**Response 200 OK**
```json
{
  "success": true,
  "data": {},
  "message": "Account updated successfully"
}
```

**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "Account not found",
  "error": "ACCOUNT_NOT_FOUND"
}
```
---
### DELETE /api/v1/finance/accounts/:id
**Response 200 OK**
```json
{
  "success": true,
  "data": {},
  "message": "Account deleted successfully"
}
```

**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "Account not found",
  "error": "ACCOUNT_NOT_FOUND"
}
```
---
### GET `/api/v1/finance/transactions`
Retrieve all transactional data

**Query Parameters**:
- page (int, optional): page number, starting from 0, default 0.
- limit (int, optional): item per page, default 10.

**Response 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "type": "EXPENSE",
      "account": {
        "name": "wallet",
        "type": "cash"
      },
      "category_id": {
        "type" : "EXPENSE",
        "name" : "Food",
        "icon" : "someplaceholderurl"
      },
      "amount": 10,
      "date": "timestamp",
      "title": "Lunch",
      "note": "Subway, forgot to bring lunchbox",
    },

    {
      "id": 2,
      "type": "INCOME",
      "account": {
        "name": "wallet",
        "type": "cash"
      },
      "category_id": {
        "type" : "INCOME",
        "name" : "Allowance",
        "icon" : "someplaceholderurl"
      },
      "amount": 10,
      "date": "timestamp",
      "title": "",
      "note": "Daily allowance",
    }
  ],
  "message": "finance retrieved successfully"
}
```
---
### POST /api/v1/finance/transactions
**Request Body**
```json
{
  "type": "EXPENSE",
  "account_id": 1,
  "category_id": 1,
  "amount": 15.0,
  "date": 1618579200,
  "title": "Lunch",
  "note": "Nasi Padang"
}
```

**Response 201 Created**
```json
{
  "success": true,
  "data": {
    "id": 1
  },
  "message": "Transaction created successfully"
}
```

**Response 400 Bad Request**
```json
{
  "success": false,
  "data": {
    "amount": "Amount must be greater than 0"
  },
  "message": "Please correct the highlighted fields",
  "error": "VALIDATION_ERROR"
}
```
---
### PUT /api/v1/finance/transactions/:id
**Request Body**
```json
{
  "amount": 20.0
}
```

**Response 200 OK**
```json
{
  "success": true,
  "data": {},
  "message": "Transaction updated successfully"
}
```

**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "Transaction not found",
  "error": "TRANSACTION_NOT_FOUND"
}
```
---
### DELETE /api/v1/finance/transactions/:id
**Response 200 OK**
```json
{
  "success": true,
  "data": {},
  "message": "Transaction deleted successfully"
}
```
**Response 404 Not Found**
```json
{
  "success": false,
  "data": {},
  "message": "Transaction not found",
  "error": "TRANSACTION_NOT_FOUND"
}
```
---

## Validation Rules

| Field| Rule  |
|------|-------|
| type | Required |
| account_id | Required |
| category_id | Required |
| amount | Required |
| date | Required |

## Additional Notes
- Modifying account balance should add "Correction" transaction to balance it out
- Editing or deleting transaction should result in change to account balance