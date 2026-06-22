# Property Management System

A Django-based property management web application with geospatial search, vector embeddings, and PostgreSQL.

---

## Tech Stack

- **Backend** — Django, Django REST Framework
- **Database** — PostgreSQL + PostGIS + pgvector
- **Geospatial** — GeoDjango (`django.contrib.gis`)
- **Containerization** — Docker & Docker Compose

---

## Features

- Property listings with geo-coordinates and polygon footprints
- Location-based radius search (lat/lng + km)
- City-based filtering
- Vector embeddings (HNSW index) for semantic search readiness
- Property image management with metadata
- Django Admin interface

---

## Project Structure

```
Property-Management-System/
├── config/               # Django settings, URLs, WSGI/ASGI
├── property_app/         # Core app (models, views, URLs, templates)
│   ├── models.py         # Location, Property, PropertyImage
│   ├── views.py          # Home, List, Detail views
│   └── urls.py           # App URL routes
├── docker/
│   ├── django/           # Django Dockerfile
│   └── postgres/         # PostgreSQL + PostGIS Dockerfile & init SQL
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose installed

### 1. Clone the repository

```bash
git clone https://github.com/sabbirhosen44/Property-Management-System.git
cd Property-Management-System
```

### 2. Create a `.env` file

```env
POSTGRES_DB=property_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
```

### 3. Start the containers

```bash
docker-compose up --build
```

### 4. Run migrations

```bash
docker exec -it property_web python manage.py migrate
```

### 5. Create a superuser

```bash
docker exec -it property_web python manage.py createsuperuser
```

### 6. Start the development server

```bash
docker exec -it property_web python manage.py runserver 0.0.0.0:8000
```

Visit [http://localhost:8000](http://localhost:8000)

---

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | `HomeView` | Homepage with featured properties |
| `/properties/` | `PropertyListView` | Paginated property list with filters |
| `/properties/<slug>/` | `PropertyDetailView` | Single property detail |

### Query Parameters (Property List)

| Parameter | Description |
|-----------|-------------|
| `city` | Filter by city name |
| `lat`, `lng` | Center point for radius search |
| `radius` | Search radius in km (default: 5) |

---

## Models

- **Location** — Named geographic area with point + polygon boundary and vector embedding
- **Property** — Listing with type, status, price, bedroom/bathroom count, geo-point, footprint, and HNSW-indexed embedding
- **PropertyImage** — Images linked to a property with alt text, dimensions, file size, and image embedding

---

## License

MIT
