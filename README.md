# CRM Campaign API

## 🚀 Features

* Create and list marketing campaigns with validation
* Retrieve users by segment
* In-memory data storage, no external database required
* API key authentication on all endpoints via `X-API-Key` header

---

## 🔐 Authentication

All API requests require a valid API key sent in the header:

```
X-API-Key: super-secret-key
```

Requests without a valid key will receive a 401 Unauthorized response.

---

## 🐳 Docker

Install Docker then build and run the application container:

```bash
docker build -t crm-campaign-api .
docker run -p 8000:8000 crm-campaign-api
```

Access the API at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🧪 Running Tests

Run all tests with:

```bash
docker build -t crm-campaign-api .
docker run --rm crm-campaign-api pytest -q
```

---

## 📘 API Endpoints

| Method | Endpoint                       | Description               |
| ------ | ------------------------------ | ------------------------- |
| POST   | `/campaigns`                   | Create a new campaign     |
| GET    | `/campaigns`                   | List all campaigns        |
| GET    | `/campaigns/{id}`              | Retrieve a campaign by ID |
| GET    | `/segments/{segment_id}/users` | List users in a segment   |

---

## ⚙️ Example Usage

### Create a campaign

```bash
curl -X POST http://localhost:8000/campaigns \
  -H "X-API-Key: super-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"name":"Summer Sale","start_date":"2025-07-01","end_date":"2025-07-15","segment_id":101}'
```

### List campaigns

```bash
curl -H "X-API-Key: super-secret-key" http://localhost:8000/campaigns
```

---

## 📂 Project Structure

* `app/models/` — Pydantic models for data validation
* `app/services/` — Business logic services
* `app/routers/` — API route definitions
* `app/storage/db.py` — In-memory data storage
* `app/core/auth.py` — API key validation
* `app/core/exception_handlers.py` — Custom error handlers
* `tests/` — Unit and integration tests
