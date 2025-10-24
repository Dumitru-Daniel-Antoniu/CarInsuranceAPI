# Car Insurance API

## Overview

Car Insurance API is a backend service for managing car insurance policies and claims. It provides RESTful endpoints for creating, retrieving, and validating car insurance policies, submitting claims, and accessing historical data. The system includes scheduled tasks for marking expired policies.

## Technologies Used

- **Python**
- **Django REST Framework**
- **SQLAlchemy**
- **APScheduler**
- **SQLite** 

## API Endpoints

### Car Endpoints

#### POST /api/cars
Create a new car.  
**Responses:**
- `201 Created` – Car created successfully.
- `409 Conflict` – VIN must be unique.
- `422 Unprocessable Content` – mandatory fields must contain correct data type.

**Error Example:**
```json
{
    "error": {
        "code": 409,
        "message": "VIN must be unique",
        "details": null
    }
}
```

#### GET /api/cars/{car_id}
Retrieve car details.  
**Responses:**
- `200 OK` – Car found.
- `404 Not Found` – Car does not exist.

**Error Example:**
```json
{
    "error": {
        "code": 404,
        "message": "Car not found",
        "details": null
    }
}
```

---

### Policy Endpoints

#### POST /api/cars/{car_id}/policies
Create a new policy.  
**Responses:**
- `201 Created` – Policy created successfully.
- `422 Unprocessable Entity` – Validation errors.

**Error Example:**
```json
{
    "error": {
        "code": 422,
        "message": "Policy validation error",
        "details": "Value error, Date must be between 1900 and 2100."
    }
}
```

#### GET api/cars/{car_id}/policies/{policy_id}
Retrieve policy details.  
**Responses:**
- `200 OK` – Policy found.
- `404 Not Found` – Policy or car does not exist.

---

### Validity Endpoint

#### GET /api/cars/{car_id}/insurance-valid/?date={date}
Check if a car has a valid policy on a given date.  
**Responses:**
- `200 OK` – Returns `{ "valid": true/false }`.
- `400 Bad Request` – Invalid date format.
- `404 Not Found` – Car does not exist.

---

### Claims Endpoints

#### POST /api/cars/{car_id}/claims
Submit a claim.  
**Responses:**
- `201 Created` – Claim created successfully (with `Location` header).
- `400 Bad Request` – Invalid fields.
- `404 Not Found` – Car does not exist.

---

### History Endpoint

#### GET /api/cars/{car_id}/history
Retrieve historical events for a car, ordered by date.  
**Responses:**
- `200 OK` – Returns list of historical events.
- `404 Not Found` – Car does not exist.

---

## Scheduled Tasks

The API includes scheduled background tasks for automatically marking expired policies. This is managed using **APScheduler** and runs periodically to ensure policy statuses remain accurate.

---

## OpenAPI Documentation

The API includes auto-generated OpenAPI documentation, accessible through:

- **`/docs`** – Interactive Swagger UI
- **`/openapi.json`** – Raw OpenAPI schema

---

## Error Handling

All errors follow a consistent JSON format:

```json
{
    "error": {
        "code": <status_code>,
        "message": "<error_message>",
        "details": "<optional_details>"
    }
}
```

### Common Error Examples

- Car not found:
```json
{
    "error": {
        "code": 404,
        "message": "Car not found",
        "details": null
    }
}
```

- VIN must be unique:
```json
{
    "error": {
        "code": 409,
        "message": "VIN must be unique",
        "details": null
    }
}
```

- Policy validation error:
```json
{
    "error": {
        "code": 422,
        "message": "Policy validation error",
        "details": "Value error, Date must be between 1900 and 2100."
    }
}
```

---

## Running the Server

To start the development server, run:

```bash
python manage.py runserver
```

By default, the API will start locally on `http://127.0.0.1:8000`.
