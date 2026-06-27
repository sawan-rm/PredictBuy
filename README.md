# Recommendation System API

## Overview

A Django REST Framework based recommendation system that manages Products, Users, and User Interactions through RESTful APIs.

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite (Development)

## API Architecture

The project uses:

* DRF ModelViewSet
* DefaultRouter
* ModelSerializer
* SearchFilter
* OrderingFilter

Router automatically generates CRUD endpoints for each ViewSet.

## Endpoints

### Products

| Method | Endpoint        | Description       |
| ------ | --------------- | ----------------- |
| GET    | /products/      | List all products |
| POST   | /products/      | Create a product  |
| GET    | /products/{id}/ | Retrieve product  |
| PUT    | /products/{id}/ | Update product    |
| DELETE | /products/{id}/ | Delete product    |

### Users

| Method | Endpoint     | Description    |
| ------ | ------------ | -------------- |
| GET    | /users/      | List all users |
| POST   | /users/      | Create a user  |
| GET    | /users/{id}/ | Retrieve user  |
| PUT    | /users/{id}/ | Update user    |
| DELETE | /users/{id}/ | Delete user    |

### Interactions

| Method | Endpoint            | Description          |
| ------ | ------------------- | -------------------- |
| GET    | /interactions/      | List interactions    |
| POST   | /interactions/      | Create interaction   |
| GET    | /interactions/{id}/ | Retrieve interaction |
| PUT    | /interactions/{id}/ | Update interaction   |
| DELETE | /interactions/{id}/ | Delete interaction   |

## Search

Products can be searched using:

GET /products/?search=laptop

Searchable fields:

* name
* category
* description

## Ordering

Products can be ordered using:

GET /products/?ordering=price

Available ordering fields:

* price
* created_at

## How Routing Works

DefaultRouter registers ViewSets and automatically creates RESTful routes.

Example:

router.register('products', ProductViewSet)

Automatically generates:

* GET /products/
* POST /products/
* GET /products/{id}/
* PUT /products/{id}/
* PATCH /products/{id}/
* DELETE /products/{id}/

<!-- -------------------------------------------- -->
## DRF Concepts Used

- ModelSerializer
- ModelViewSet
- DefaultRouter
- SearchFilter
- OrderingFilter
- ORM Queries
- CRUD Operations
