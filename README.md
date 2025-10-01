# Django ML App

A minimal **Django 5** web app that serves a **scikit-learn RandomForest** model trained on *Iris*.
You get:

* Web form to submit features and view predictions
* JSON API endpoint (`POST /api/predict/`)
* Simple training script (`train.py`)
* Tests and dev tooling (optional)

## Features

* 🔮 Predict Iris species with probabilities
* 🧠 Local training with `scikit-learn`; model saved via `joblib`
* 🌐 Django views + basic JSON API
* ⚡ Uses **uv** for fast installs and a local **venv**
* ✅ Unit tests (`pytest` optional)



## Tech Stack

* Python 3.10+
* Django ≥ 5.0
* scikit-learn, joblib
* uv (package + venv manager)



## Project Layout

```
django-ml-app/
├─ .venv/                          # local virtual env (created by uv)
├─ manage.py
├─ requirements.txt
├─ train.py                        # trains & saves the model
├─ mymlsite/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py                  # add 'predictor' to INSTALLED_APPS
│  ├─ urls.py                      # routes include predictor.urls
│  └─ wsgi.py
├─ predictor/
│  ├─ __init__.py
│  ├─ apps.py
│  ├─ forms.py                     # IrisForm
│  ├─ services.py                  # lazy model load + predict
│  ├─ urls.py
│  ├─ views.py                     # web form + JSON API
│  ├─ tests.py
│  └─ model/
│     └─ iris_rf.joblib            # created by train.py
└─ templates/
   └─ predictor/
      └─ predict_form.html
```



## Quickstart

### 1) Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

uv --version
```

### 2) Create & activate a local venv

```bash
uv venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
uv pip install "Django>=5.0" scikit-learn joblib
# (optional dev tools)
uv pip install pytest pytest-django black isort
uv pip freeze > requirements.txt
```

### 4) Train the model

```bash
python train.py
# -> creates predictor/model/iris_rf.joblib
```

### 5) Run the app

```bash
python manage.py migrate
python manage.py runserver
```

Open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)



## API

### Endpoint

`POST /api/predict/`
Content-Type: `application/json` (recommended)

**Request body**

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response**

```json
{
  "class_index": 0,
  "class_name": "setosa",
  "probabilities": {
    "setosa": 0.97,
    "versicolor": 0.02,
    "virginica": 0.01
  }
}
```

**curl example**

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

> CSRF: This API view is annotated with `@csrf_exempt` so scripts like `curl` work by default. For browser-session APIs, prefer token/JWT auth (see “Security & Production” below).



## Web UI

* Home (`/`) renders a simple form (`templates/predictor/predict_form.html`)
* Submits to `/predict/`
* Displays predicted class + per-class probabilities
<img width="1639" height="902" alt="Screenshot 2025-09-09 015539" src="https://github.com/user-attachments/assets/23008c5a-d2c3-4169-a9a7-6116cb34c69a" />



## Configuration

* **Django settings**: `mymlsite/settings.py`

  * Ensure `INSTALLED_APPS` includes `"predictor"`
  * Template dir includes `BASE_DIR / "templates"`
* **Model path**: `predictor/model/iris_rf.joblib` (created by `train.py`)
* **Allowed hosts (dev)**:

  ```python
  ALLOWED_HOSTS = ["*"]  # dev only
  ```



## Testing

With Django’s test runner:

```bash
python manage.py test
```

Or with `pytest`:

```bash
pytest
```



## Common Tasks (uv + venv)

```bash
# Install from requirements
uv pip install -r requirements.txt

# Add a new package later
uv pip install djangorestframework
uv pip freeze > requirements.txt

# Recreate env elsewhere
uv venv .venv
source .venv/bin/activate   # or .venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```



## Troubleshooting

**403 Forbidden — CSRF verification failed**
You’re calling the API without a CSRF token while CSRF is enforced.
This repo’s `predict_api` uses `@csrf_exempt`. If you removed that, either:

* Send a CSRF token (fetch `/` to get cookie, post with `X-CSRFToken`), or
* Use token/JWT auth for APIs and keep CSRF for browser forms only.

**Model not found / `FileNotFoundError`**
Run `python train.py` before serving; confirm `predictor/model/iris_rf.joblib` exists.

**Import/Module errors**
Ensure your virtual environment is active: `source .venv/bin/activate` (or Windows variant).



## Security & Production

* Set `DEBUG=False` and proper `ALLOWED_HOSTS`.
* Use a real database (e.g., Postgres) and configure static files.
* Prefer **token/JWT auth** (e.g., Django REST Framework) for APIs; CSRF is for browser sessions.
* Consider rate limiting, input validation, and basic auth for public endpoints.
* Example WSGI:

  ```bash
  uv pip install gunicorn
  gunicorn mymlsite.wsgi:application --bind 0.0.0.0:8000
  ```



## Extending

* Swap the Iris model for your own dataset + pipeline
* Add Django REST Framework with OpenAPI schema
* Frontend polish (HTMX/Alpine/React)
* Containerize (Docker) and deploy behind Nginx



## Scripts & Handy Commands

```bash
# Run server
python manage.py runserver

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

```


