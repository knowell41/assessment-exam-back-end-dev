# Assessment Exam Back-End

This is a Django REST API project for a blogging platform, featuring user authentication (JWT), post and comment management, and API documentation with Swagger. The project is containerized with Docker and uses Poetry for dependency management.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Admin Panel](#admin-panel)
- [Project Details](#project-details)
- [License](#license)

---

## Features

- JWT authentication
- CRUD operations for blog posts
- Commenting system for posts
- Filtering and searching posts by author, title, content, status, and published date
- Pagination for post listings
- API documentation via Swagger (drf-yasg)
- Admin panel for managing users, posts, and comments
- CORS support
- Static file serving with WhiteNoise
- Dockerized for easy deployment

---

## Project Structure

```
.
├── blog/                # Blog app: models, views, serializers, tests
├── server/              # Django project settings, URLs, ASGI/WSGI
├── static/              # Static files (admin, drf-yasg, rest_framework)
├── template/            # HTML templates
├── .env                 # Environment variables (not committed)
├── compose.yml          # Docker Compose configuration
├── Dockerfile           # Docker build instructions
├── entrypoint.sh        # Entrypoint script for Docker
├── manage.py            # Django management script
├── poetry.lock          # Poetry lock file
├── pyproject.toml       # Poetry project file
└── README.md            # Project documentation
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) (optional, for containerized setup)

### Local Development

1. **Clone the repository:**

   ```sh
   git clone https://github.com/knowell41/assessment-exam-back-end-dev.git
   cd assessment-exam-back-end-dev
   ```

2. **Install dependencies:**

   ```sh
   poetry install
   ```

3. **Set up environment variables:**

   - Copy `env-example` to `.env` and adjust values as needed.

4. **Apply migrations:**

   ```sh
   poetry run python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**

   ```sh
   poetry run python manage.py createsuperuser
   ```

6. **Collect static files:**

   ```sh
   poetry run python manage.py collectstatic --no-input
   ```

7. **Run the development server:**
   ```sh
   poetry run python manage.py runserver
   ```

---

## Environment Variables

See `env-example` for all available environment variables. Key variables include:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `True` for development
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `JWT_SECRET_KEY`: Secret for JWT signing (optional, defaults to `SECRET_KEY`)
- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`: For automatic superuser creation in Docker

---

## Running the Project

### With Docker

1. **Build and start the containers:**

   ```sh
   docker compose up --build
   ```

2. **Access the application:**
   - Landing Page: http://localhost/
   - Admin: http://localhost/admin/
   - Swagger: http://localhost/swagger/

---

## API Documentation

Interactive API docs are available at [http://localhost/swagger/](http://localhost/swagger/) (powered by drf-yasg).

---

## Testing

Run all tests using Django's test runner:

```sh
poetry run python manage.py test
```

Tests are located in [`blog/tests.py`](blog/tests.py).

---

## Admin Panel

The Django admin panel is available at [http://localhost/admin/](http://localhost/admin/).

- Use default admin user defined in the `.env` file as login credential `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD`
- Manage users, authors, posts, and comments.
- Requires superuser credentials.

---

## Project Details

- **Posts**: Have title, content, author, published date, status (`draft`/`published`), and active flag.
- **Comments**: Linked to posts and users (optional for anonymous).
- **Authentication**: JWT-based, using `rest_framework_simplejwt`.
- **Filtering**: Posts can be filtered by author name, title, content, status, published date, and active status.
- **Pagination**: Default page size is 10.

See [`blog/api.py`](blog/api.py) and [`blog/serializers.py`](blog/serializers.py) for API and serialization logic.

---

## License

This project is licensed under the MIT License.
