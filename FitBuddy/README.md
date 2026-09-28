# FitBuddy — AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite web application that generates personalized 7-day fitness plans, nutrition/recovery tips, and feedback-based plan revisions using Google Gemini.

The project follows the supplied documentation's architecture:
- Frontend: HTML + Jinja2
- Backend: FastAPI
- AI layer: Google Gemini
- Database: SQLite + SQLAlchemy
- Pages: `index.html`, `result.html`, `all_users.html`
- Core flows: generate plan, update by feedback, nutrition/recovery tip, admin dashboard

## Important modernization

The original project documentation names Gemini 1.5 Pro and a generic Gemini Flash model. Those model names are historical. This implementation uses the current Google GenAI Python SDK (`google-genai`) and configurable model IDs in `.env`.

Default models:
- Workout/revision: `gemini-3.8-flash`
- Nutrition/recovery: `gemini-3.5-flash-lite`

You can change these values without editing application code.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── ai_client.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── all_users.html
│   ├── base.html
│   ├── index.html
│   └── result.html
├── tests/
│   └── test_app.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## 1. VS Code setup

Install:
1. Python 3.11+ (3.12 recommended)
2. VS Code
3. VS Code Python extension

Open the `FitBuddy` folder in VS Code.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Configure Gemini

Copy `.env.example` to `.env`.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

Put your Gemini API key into:

```env
GEMINI_API_KEY=your_real_key
```

Google's current Gemini Python examples use the `google-genai` package and `genai.Client`, with the API key supplied through environment configuration. See the official Gemini documentation:
- https://ai.google.dev/gemini-api/docs/get-started
- https://ai.google.dev/gemini-api/docs/models

For a no-key demo, use:

```env
USE_MOCK_AI=true
```

This lets you test the complete frontend/backend/database flow without calling Gemini.

## 3. Run the application

From the project root:

```bash
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000 — FitBuddy UI
- http://127.0.0.1:8000/docs — Swagger API documentation
- http://127.0.0.1:8000/redoc — ReDoc API documentation
- http://127.0.0.1:8000/view-all-users — admin dashboard

The SQLite database file `fitbuddy.db` is created automatically on first startup.

## 4. Test the full workflow

### A. Generate a plan

Enter:
- User ID: `demo01`
- Name: `Sameema`
- Age: `20`
- Weight: `55`
- Goal: `general wellness`
- Intensity: `medium`

Click **Generate 7-Day Plan**.

You should see:
- user information
- a seven-day plan
- nutrition/recovery advice
- a feedback form

### B. Update the plan

Enter feedback such as:

```text
Add more cardio, keep the sessions under 40 minutes, and include another recovery day.
```

Submit it. The app retrieves the stored plan, asks Gemini to revise it, stores the updated version, and displays the revised plan.

### C. Check the API

Open `/docs`.

Useful endpoints:
- `GET /api/health`
- `GET /api/users/{user_id}`
- `POST /generate-workout`
- `POST /submit-feedback`

### D. Check admin

Open `/view-all-users`.

The browser will request the configured Basic Auth credentials:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me
```

Change the password before sharing or deploying the app.

## 5. Run automated tests

With the virtual environment activated:

```bash
pytest -q
```

The tests intentionally use `USE_MOCK_AI=true`, so they do not spend API quota and do not require a Gemini key.

## 6. Docker

Build:

```bash
docker build -t fitbuddy .
```

Run:

```bash
docker run --rm -p 8000:8000 --env-file .env fitbuddy
```

Then open http://127.0.0.1:8000.

## 7. API examples

### Generate workout

```bash
curl -X POST http://127.0.0.1:8000/generate-workout \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "user_id=demo02" \
  --data-urlencode "name=Alex" \
  --data-urlencode "age=25" \
  --data-urlencode "weight=70" \
  --data-urlencode "goal=muscle gain" \
  --data-urlencode "intensity=medium"
```

### Get stored user data

```bash
curl http://127.0.0.1:8000/api/users/demo02
```

## 8. How the code is organized

- `app/routes.py`: HTTP routes and orchestration
- `app/schemas.py`: input validation
- `app/models.py`: SQLAlchemy database models
- `app/crud.py`: database operations
- `app/gemini_generator.py`: seven-day workout generation
- `app/gemini_flash_generator.py`: nutrition/recovery tip generation
- `app/updated_plan.py`: feedback-based plan revision
- `app/ai_client.py`: single Gemini integration point plus local mock mode
- `templates/`: Jinja2 frontend
- `static/css/styles.css`: responsive UI
- `tests/test_app.py`: end-to-end route tests

## 9. Troubleshooting

### `ModuleNotFoundError`

Make sure VS Code is using the `.venv` interpreter:
- `Ctrl+Shift+P`
- **Python: Select Interpreter**
- select `.venv`

Then run:

```bash
pip install -r requirements.txt
```

### Gemini API errors

First confirm:

```env
GEMINI_API_KEY=...
USE_MOCK_AI=false
```

If you want to verify the app independently of Gemini:

```env
USE_MOCK_AI=true
```

If the selected model is unavailable for your account, change `WORKOUT_MODEL` or `NUTRITION_MODEL` to a model available to your Gemini API project.

### Admin page returns 401

Use the credentials from `.env`:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me
```

Restart the server after changing `.env`.

### Database reset

Stop the server and delete `fitbuddy.db`, then start the app again. The schema is recreated automatically.

## Safety note

FitBuddy is an educational wellness application. Generated plans should be treated as general information rather than medical advice. The prompts explicitly instruct the model to avoid diagnosis, medication advice, extreme dieting, and unsafe exercise recommendations.
