# Bharath FD 

## Overview
This project provides a multilingual FAQ API built with Django and Django REST Framework (DRF). It supports caching for optimized performance and includes translations for Hindi and Bengali with English as a fallback.

## Features
- API for retrieving FAQs with multilingual support
- Caching for improved performance
- Dockerized deployment for easy setup
- Unit tests to ensure API correctness

---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- Docker & Docker Compose
- Git

### Clone the Repository
```sh
git clone https://github.com/your-repo/faq-api.git
cd faq-api
```

### Setup Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Apply Migrations
```sh
python manage.py migrate
```

### Run Tests
```sh
python manage.py test
```

---

## Running the Project

### Running Locally
```sh
python manage.py runserver
```

### Running with Docker
Build and start the container:
```sh
docker build -t faq-api .
docker run -p 8000:8000 faq-api
```

Alternatively, using Docker Compose:
```sh
docker-compose up --build
```

---

## API Usage

### Get FAQs
```http
GET /api/faqs/?lang=hi  # Fetch FAQs in Hindi
GET /api/faqs/?lang=bn  # Fetch FAQs in Bengali
GET /api/faqs/  # Fetch FAQs in English (default)
```

#### Example Response
```json
[
  {
    "id": 1,
    "question": "What is Django?",
    "answer": "Django is a web framework."
  }
]
```

---

## Caching
This project uses Django's caching framework to store translations. To clear the cache manually:
```sh
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## Deployment
Modify `.env` for production settings, then run:
```sh
docker-compose -f docker-compose.prod.yml up --build -d
```

---

## Git Best Practices

### Creating Commits
```sh
git add .
git commit -m "Your meaningful commit message"
git push origin main
```

### Branching Strategy
- `main`: Stable production branch
- `dev`: Active development branch
- Feature branches: `feature/<feature-name>`
- Bug fixes: `fix/<issue-name>`

---

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

## License
Mozilla 

