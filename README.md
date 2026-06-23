# Property Management System

A Django-based Property Management System built with GeoDjango, PostGIS, PGVector, and Sentence Transformers. The application supports geospatial property search, semantic location search, vector embeddings, and property management through an admin dashboard.

---

## Features

### Property Management

- Property CRUD management
- Property image management
- Property status and type management
- Featured property support

### Geospatial Search

- GeoDjango integration
- PostGIS-powered geographic queries
- Radius-based property search
- Distance calculation between locations and properties
- City-based property filtering

### Semantic Search

- Sentence Transformers integration
- Location embeddings generation
- PGVector vector storage
- HNSW vector indexing
- Semantic location search
- Semantic autocomplete API

### User Interface

- Homepage with property search
- Property listing page with pagination
- Property detail page
- Responsive frontend design

### Administration

- Django Admin dashboard
- Location management
- Property management
- Image management

---

## Tech Stack

### Backend

* Django
* Django REST Framework

### Database

* PostgreSQL
* PostGIS
* PGVector

### AI & Search

* Sentence Transformers
* all-MiniLM-L6-v2
* HNSW Index

### Geospatial

* GeoDjango

### DevOps

* Docker
* Docker Compose

---

## Project Structure

```text
property-management-system/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── property_app/
│   ├── management/
│   │   └── commands/
│   │       ├── import_properties.py
│   │       └── generate_location_embeddings.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
│   │   └── semantic_search_service.py
│   │
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── media/
├── data/
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

## Prerequisites

Install:

* Docker
* Docker Compose

Verify installation:

```bash
docker --version
docker compose version
```

---

## Clone Repository

```bash
git clone https://github.com/sabbirhosen44/Property-Management-System.git

cd Property-Management-System
```

---

## Environment Variables

Create a `.env` file:

```env
POSTGRES_DB=propertydb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## Build Containers

```bash
docker compose build
```

Or rebuild completely:

```bash
docker compose down

docker compose build --no-cache

docker compose up -d
```

---

## Start Containers

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

---

## Run Database Migrations

```bash
docker compose exec web python manage.py makemigrations

docker compose exec web python manage.py migrate
```

---

## Create Admin User

```bash
docker compose exec web python manage.py createsuperuser
```

Access:

```text
http://localhost:8000/admin/
```

---

## Import Property Data

Example:

```bash
docker compose exec web python manage.py import_properties data/properties.csv
```

Verify:

```bash
docker compose exec web python manage.py shell
```

```python
from property_app.models import Property

Property.objects.count()
```

---

## Run Development Server
```bash
docker compose exec web python manage.py runserver 0.0.0.0:8000
```

Access:

```text
http://localhost:8000/
```


## Generate Location Embeddings

Open a new terminal and Generate embeddings for all locations:

```bash
docker compose exec web python manage.py generate_location_embeddings
```

---

## Running Django Shell

```bash
docker compose exec web python manage.py shell
```

---

## Semantic Search Testing

Inside Django shell:

```python
from property_app.services.semantic_search_service import SemanticSearchService
```

Search examples:

```python
SemanticSearchService.search("beach")
```

```python
SemanticSearchService.search("hill")
```

```python
SemanticSearchService.search("lake")
```

```python
SemanticSearchService.search("tea garden")
```

```python
SemanticSearchService.search("wildlife")
```

Example output:

```text
beach       -> Cox's Bazar
hill        -> Bandarban
lake        -> Gazipur
tea garden  -> Sylhet
wildlife    -> Khulna
```

---

## Available URLs

| URL                 | Description               |
| ------------------- | ------------------------- |
| /                   | Homepage                  |
| /properties/        | Property Listing          |
| /properties/<slug>/ | Property Details          |
| /api/cities/        | Location Autocomplete API |
| /admin/             | Django Admin              |

---

## Geo Search Examples

City Search:

```text
http://localhost:8000/properties/?city=Dhaka
```

Radius Search:

```text
http://localhost:8000/properties/?lat=23.8103&lng=90.4125&radius=10
```

---

## Useful Commands

Stop containers:

```bash
docker compose down
```

Restart containers:

```bash
docker compose restart
```

Open Django shell:

```bash
docker compose exec web python manage.py shell
```

Open PostgreSQL:

```bash
docker compose exec db psql -U postgres -d propertydb
```

---

## Author

Md. Sabbir Hosen
