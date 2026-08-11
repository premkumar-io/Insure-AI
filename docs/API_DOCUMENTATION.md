# 📡 InsureAI™ API Documentation v2.0.0

Complete REST API reference for the **InsureAI™** Insurance Premium Category Prediction service powered by FastAPI and Uvicorn.

---

## 🌐 Base Server URLs

- **Local Development**: `http://localhost:8000`
- **Swagger Interactive UI**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 📌 Endpoints Summary

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Home & Service Info | None |
| `GET` | `/health` | Health Check & Model Status | None |
| `POST` | `/predict` | Predict Insurance Premium Category | None |

---

## 1. Health Check Endpoint

### `GET /health`
Returns status of the FastAPI service and model loading state.

#### Request Example
```bash
curl -X GET "http://localhost:8000/health"
```

#### Response Example (200 OK)
```json
{
  "status": "OK",
  "version": "2.0.0",
  "model_loaded": true
}
```

---

## 2. Prediction Endpoint

### `POST /predict`
Evaluates applicant demographics and physical metrics to predict the insurance premium category (**Low**, **Medium**, or **High**) along with confidence score and class probabilities.

#### Request Headers
`Content-Type: application/json`

#### Request Body Schema (`UserInput`)

```json
{
  "age": 30,
  "weight": 68.0,
  "height": 1.75,
  "income_lpa": 14.0,
  "smoker": false,
  "city": "Bangalore",
  "occupation": "private_job"
}
```

#### Parameter Validation Rules

| Parameter | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `age` | `integer` | Yes | $1 \le \text{age} < 120$ | Age of applicant in years |
| `weight` | `float` | Yes | $0.0 < \text{weight} \le 500.0$ kg | Body weight in kilograms (finite) |
| `height` | `float` | Yes | $0.5 \le \text{height} \le 2.5$ meters | Height in meters (finite) |
| `income_lpa` | `float` | Yes | $0.0 < \text{income\_lpa} \le 10000.0$ LPA | Annual income in LPA (₹, finite) |
| `smoker` | `boolean` | Yes | `true` or `false` | Active tobacco/smoking habit |
| `city` | `string` | Yes | Non-empty string | Residential city (auto-normalized) |
| `occupation` | `string` | Yes | Enum: `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job` | Employment category |

#### Response Schema (`PredictionResponse`)

##### Success Response (200 OK)
```json
{
  "predicted_category": "Low",
  "confidence": 0.78,
  "class_probabilities": {
    "High": 0.02,
    "Low": 0.78,
    "Medium": 0.20
  }
}
```

##### Validation Error Response (422 Unprocessable Entity)
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Please check the highlighted input fields.",
    "details": [
      {
        "field": "age",
        "message": "Input should be greater than 0",
        "type": "greater_than"
      }
    ]
  }
}
```

##### Server Error Response (500 Internal Server Error)
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred while generating prediction. Please try again later."
  }
}
```

---

## 🔒 CORS & Security Policy
FastAPI is configured with `CORSMiddleware` supporting configurable cross-origin requests via the `ALLOWED_ORIGINS` environment variable.
