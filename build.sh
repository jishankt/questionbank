#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**`Procfile`** — create this file:
```
web: gunicorn questionbank.wsgi:application