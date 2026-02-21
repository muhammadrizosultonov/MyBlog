# Muhammadrizo Portfolio + Blog

Production-ready personal portfolio and blog platform.

## Stack
- Python 3.11+
- Django 5+
- Django REST Framework
- PostgreSQL (prod) / SQLite (dev)
- TailwindCSS (CDN + config for build)
- HTMX, Alpine.js, AOS
- Markdownx
- OpenAI API integration
- Celery + Redis structure

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Tailwind (optional build)
CDN is used by default. For production builds, wire a Tailwind CLI or build pipeline using `tailwind.config.js`.

## Apps
- `me`: home/about/contact pages + profile content
- `apps/portfolio`: projects
- `apps/blog`: posts, RSS, markdown
- `apps/ai`: AI assistant API + logs
- `apps/core`: shared context + SEO assets

## AI Assistant
Endpoint: `/api/chat/`
- Providers: Groq (default) or OpenAI fallback
- Uses `AI_PROVIDER`, `GROQ_API_KEY`, `GROQ_MODEL`, optional `OPENAI_API_KEY`
- Grounded responses from Profile + Projects + BlogPosts
- Rate limiting (20/min/IP)
- Caches answers for 1 hour (configurable)

## Docker
```bash
docker compose up --build
```

## Settings & Environments
Settings are split into:
- `conf/settings/base.py`
- `conf/settings/dev.py` (default)
- `conf/settings/prod.py`

Run dev:
```bash
export DJANGO_SETTINGS_MODULE=conf.settings.dev
python manage.py runserver
```

Simulate prod:
```bash
export DJANGO_SETTINGS_MODULE=conf.settings.prod
python manage.py check --deploy
```

## Environment
See `.env.example` for required variables.
