# PredictBuy

### An intelligent product recommendation engine powered by collaborative filtering.

PredictBuy is a Django REST Framework based product recommendation system that analyzes user interactions and generates personalized product recommendations using Collaborative Filtering.

The system provides RESTful APIs for managing products, users, and interactions while leveraging machine learning techniques to recommend products that users are most likely to engage with or purchase.

---

## Features

* Personalized Product Recommendations
* User-Based Collaborative Filtering
* Product Management APIs
* User Management APIs
* Interaction Tracking
* Search and Filtering
* Product Ordering and Sorting
* Recommendation Score Ranking
* RESTful Architecture

---

## Tech Stack

* **Backend:** Django, Django REST Framework
* **Machine Learning:** Scikit-learn (Collaborative Filtering)
* **Database:** SQLite / PostgreSQL
* **Language:** Python

---

## Project Structure

```
recommendation_system/
│
├── products/
├── recommendations/
├── recommendation_engine/
├── manage.py
└── requirements.txt
```

---

## Installation

```bash
# Clone repository
git clone <repository-url>

# Create virtual environment
python -m venv venv

# Activate virtual environment

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Load sample dataset
python manage.py load_sample_data

# Train recommendation model
python manage.py train_recommendation_model

# Run server
python manage.py runserver
```

Server starts at:

```
http://127.0.0.1:8000/
```

---

# API Endpoints

## Products

| Method | Endpoint              | Description      |
| ------ | --------------------- | ---------------- |
| GET    | `/api/products/`      | List products    |
| POST   | `/api/products/`      | Create product   |
| GET    | `/api/products/{id}/` | Retrieve product |
| PUT    | `/api/products/{id}/` | Update product   |
| PATCH  | `/api/products/{id}/` | Partial update   |
| DELETE | `/api/products/{id}/` | Delete product   |

---

## Users

| Method | Endpoint           | Description    |
| ------ | ------------------ | -------------- |
| GET    | `/api/users/`      | List users     |
| POST   | `/api/users/`      | Create user    |
| GET    | `/api/users/{id}/` | Retrieve user  |
| PUT    | `/api/users/{id}/` | Update user    |
| PATCH  | `/api/users/{id}/` | Partial update |
| DELETE | `/api/users/{id}/` | Delete user    |

---

## User Interactions

| Method | Endpoint                  | Description          |
| ------ | ------------------------- | -------------------- |
| GET    | `/api/interactions/`      | List interactions    |
| POST   | `/api/interactions/`      | Record interaction   |
| GET    | `/api/interactions/{id}/` | Retrieve interaction |
| PUT    | `/api/interactions/{id}/` | Update interaction   |
| PATCH  | `/api/interactions/{id}/` | Partial update       |
| DELETE | `/api/interactions/{id}/` | Delete interaction   |

---

## Recommendations

| Method | Endpoint                                               | Description                |
| ------ | ------------------------------------------------------ | -------------------------- |
| GET    | `/api/recommendations/?user_id=1`                      | Get recommendations        |
| GET    | `/api/recommendations/?user_id=1&count=10`             | Limit recommendation count |
| GET    | `/api/recommendations/?user_id=1&category=electronics` | Filter by category         |

---

# Search

Search products using:

```
GET /api/products/?search=laptop
```

Searchable fields:

* name
* category
* description

---

# Ordering

Sort products using:

```
GET /api/products/?ordering=price
```

Available ordering fields:

* price
* created_at

Descending order:

```
GET /api/products/?ordering=-price
```

---

# Example Requests

### Create Product

```bash
curl -X POST http://localhost:8000/api/products/ \
-H "Content-Type: application/json" \
-d '{
      "name":"iPhone",
      "category":"Electronics",
      "price":"999.99",
      "description":"Latest Apple smartphone"
    }'
```

### Get Recommendations

```bash
curl "http://localhost:8000/api/recommendations/?user_id=1&count=5"
```

---

# Recommendation Pipeline

```
User Interaction
       │
       ▼
Store in Database
       │
       ▼
Build User-Product Matrix
       │
       ▼
Calculate User Similarity
       │
       ▼
Generate Recommendation Scores
       │
       ▼
Return Top-N Products
```

---

# DRF Concepts Used

* ModelSerializer
* Serializer
* ModelViewSet
* DefaultRouter
* SearchFilter
* OrderingFilter
* Django ORM
* CRUD Operations
* Custom API Endpoints

---

# Machine Learning Concepts Used

* Collaborative Filtering
* User-Product Interaction Matrix
* Cosine Similarity
* Recommendation Score Calculation
* Top-N Recommendation Ranking

---

## Future Improvements

* Content-Based Filtering
* Hybrid Recommendation System
* JWT Authentication
* Redis Caching
* PostgreSQL Deployment
* Docker Support
* Model Retraining Pipeline

---
