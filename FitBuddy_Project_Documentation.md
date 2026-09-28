# FitBuddy Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Setup & Installation](#setup--installation)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Features](#features)
9. [Usage Guide](#usage-guide)
10. [Testing](#testing)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)

---

## Project Overview

**FitBuddy** is an intelligent fitness companion application that generates personalized workout plans and nutrition recommendations using Google's Gemini AI. Users can create fitness profiles, receive AI-generated 7-day workout plans, get nutrition tips, and update their plans based on feedback.

### Key Features
- 🏋️ AI-powered personalized workout generation
- 🥗 Nutrition and recovery recommendations
- 🔄 Feedback-based plan regeneration
- 💾 Persistent user data with SQLite
- 📊 Admin dashboard for user management
- 🔐 Basic authentication for admin access
- 🌐 Responsive web interface
- 📡 RESTful API with Swagger documentation
- 🧪 Automated test suite
- 🐳 Docker support

### Technology Stack
- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Jinja2 templates with HTML/CSS
- **AI Integration**: Google Gemini API (genai SDK)
- **Authentication**: HTTP Basic Auth
- **Testing**: pytest
- **Containerization**: Docker

---

## Architecture

### System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                     FitBuddy Application                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │   Frontend   │         │   FastAPI    │                  │
│  │ (Jinja2 HTML)├────────►│    Routes    │                  │
│  └──────────────┘         └──────┬───────┘                  │
│                                   │                          │
│                    ┌──────────────┼──────────────┐           │
│                    │              │              │           │
│              ┌─────▼────┐  ┌─────▼────┐  ┌──────▼────┐      │
│              │   CRUD   │  │   Auth   │  │  Schemas  │      │
│              │ Operations│  │ Validation│  │           │      │
│              └─────┬────┘  └────┬─────┘  └──────────┘      │
│                    │             │                          │
│                    └──────┬──────┘                          │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │  Database   │                          │
│                    │  SQLAlchemy │                          │
│                    │   SQLite    │                          │
│                    └──────┬──────┘                          │
│                           │                                 │
│              ┌────────────┼────────────┐                    │
│              │            │            │                    │
│         ┌────▼────┐  ┌───▼────┐  ┌────▼────┐               │
│         │  Users  │  │ Workouts│  │  Feedback│              │
│         │  Table  │  │  Table  │  │  Table   │              │
│         └─────────┘  └─────────┘  └──────────┘              │
│                                                               │
│  ┌──────────────────────┬────────────────────────┐           │
│  │                      │                        │           │
│  │   ┌──────────────┐   │   ┌──────────────┐    │           │
│  │   │   Gemini AI  │   │   │ Gemini Flash │    │           │
│  │   │  Generator   │   │   │  Generator   │    │           │
│  │   │ (Workouts)   │   │   │ (Nutrition)  │    │           │
│  │   └──────────────┘   │   └──────────────┘    │           │
│  │                      │                        │           │
│  │         External AI Service Layer             │           │
│  └──────────────────────┬────────────────────────┘           │
│                         │                                    │
│                  ┌──────▼──────┐                             │
│                  │   Google    │                             │
│                  │   Gemini    │                             │
│                  │    API      │                             │
│                  └─────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → User fills fitness profile form
2. **FastAPI Routes** → Receives form data, validates schemas
3. **CRUD Operations** → Stores user profile in database
4. **AI Generation** → Sends user data to Gemini AI
5. **Plan Storage** → Stores generated workout plan
6. **Response** → Returns personalized plan to user
7. **Feedback Loop** → User provides feedback, triggers regeneration
8. **Admin Dashboard** → Manages all users and their plans

---

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv)
- Google Gemini API key (from [Google AI Studio](https://aistudio.google.com))
- Git (optional)

### Step 1: Extract the Project
```bash
# Extract FitBuddy_complete_project.zip
unzip FitBuddy_complete_project.zip
cd FitBuddy
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies include:**
- fastapi
- uvicorn
- sqlalchemy
- google-generativeai
- pydantic
- python-dotenv
- pytest

### Step 4: Configure Environment

Copy the example environment file:
```bash
# Create .env from template
cp .env.example .env
```

Edit `.env` with your settings:
```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_api_key_here
WORKOUT_MODEL=gemini-2.0-flash
NUTRITION_MODEL=gemini-2.0-flash

# Database
DATABASE_URL=sqlite:///./fitbuddy.db

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me

# Development
USE_MOCK_AI=false
DEBUG=true
```

### Step 5: Run the Application
```bash
uvicorn app.main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Access Points
- **Web App**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **Admin Dashboard**: http://127.0.0.1:8000/view-all-users

---

## Project Structure

```
FitBuddy/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── ai_client.py             # AI service abstraction layer
│   ├── config.py                # Configuration management
│   ├── crud.py                  # Database CRUD operations
│   ├── database.py              # Database connection setup
│   ├── gemini_flash_generator.py # Nutrition AI generator
│   ├── gemini_generator.py       # Workout AI generator
│   ├── main.py                  # FastAPI app entry point
│   ├── models.py                # SQLAlchemy database models
│   ├── routes.py                # API endpoint definitions
│   ├── schemas.py               # Pydantic request/response schemas
│   └── updated_plan.py          # Plan update logic
│
├── templates/                    # Jinja2 HTML templates
│   ├── base.html                # Base template (header, nav)
│   ├── index.html               # Home/form page
│   ├── result.html              # Workout result page
│   └── all_users.html           # Admin dashboard
│
├── static/                       # Static files
│   ├── css/
│   │   └── styles.css           # Application styling
│   └── images/                  # Logo and assets
│
├── tests/                        # Test suite
│   └── test_app.py              # pytest test cases
│
├── .vscode/                      # VS Code configuration
│   └── settings.json            # Editor settings
│
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
├── Dockerfile                   # Docker container config
├── README.md                    # Quick start guide
├── requirements.txt             # Python dependencies
└── fitbuddy.db                  # SQLite database (auto-created)
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Google Gemini API authentication key |
| `WORKOUT_MODEL` | No | gemini-2.0-flash | Model ID for workout generation |
| `NUTRITION_MODEL` | No | gemini-2.0-flash | Model ID for nutrition tips |
| `DATABASE_URL` | No | sqlite:///./fitbuddy.db | Database connection string |
| `ADMIN_USERNAME` | No | admin | Admin dashboard login username |
| `ADMIN_PASSWORD` | No | change-me | Admin dashboard login password |
| `USE_MOCK_AI` | No | false | Enable mock AI for testing |
| `DEBUG` | No | true | Enable debug logging |

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Click "Get API Key"
3. Create a new API key
4. Copy the key to your `.env` file

### Database Configuration

The application uses SQLite by default. To use a different database:

```env
# PostgreSQL example
DATABASE_URL=postgresql://user:password@localhost/fitbuddy

# MySQL example
DATABASE_URL=mysql://user:password@localhost/fitbuddy
```

---

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api
```

### Endpoints

#### 1. Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Create User & Generate Workout
```
POST /generate-plan
Content-Type: application/json

{
  "name": "John Doe",
  "age": 28,
  "fitness_level": "intermediate",
  "goals": "build muscle and improve endurance",
  "available_days": 5,
  "equipment": "dumbbells, treadmill"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": "user_123",
  "plan": "Day 1: Chest and Triceps...",
  "nutrition_tips": "Consume 1.8g protein per kg...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 3. Get All Users (Admin)
```
GET /admin/users
Authorization: Basic admin:change-me
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 28,
      "fitness_level": "intermediate",
      "workouts": [
        {
          "id": 1,
          "plan": "Day 1: ...",
          "feedback_count": 1
        }
      ]
    }
  ],
  "total_users": 1
}
```

#### 4. Update Plan Based on Feedback
```
POST /update-plan/{user_id}
Content-Type: application/json

{
  "feedback": "The workouts are too intense. Make them more beginner-friendly."
}
```

**Response:**
```json
{
  "id": 2,
  "user_id": 1,
  "original_plan_id": 1,
  "updated_plan": "Day 1: Light Cardio...",
  "feedback": "The workouts are too intense...",
  "created_at": "2024-01-15T11:00:00Z"
}
```

#### 5. Get User's All Plans
```
GET /user/{user_id}/plans
```

**Response:**
```json
{
  "user_id": 1,
  "plans": [
    {
      "id": 1,
      "plan": "Day 1: Chest and Triceps...",
      "created_at": "2024-01-15T10:30:00Z",
      "feedback_count": 1
    }
  ]
}
```

### Error Responses

**400 Bad Request:**
```json
{
  "detail": "Invalid input data"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Invalid credentials"
}
```

**500 Server Error:**
```json
{
  "detail": "Internal server error"
}
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(100) NOT NULL,
  age INTEGER NOT NULL,
  fitness_level VARCHAR(50) NOT NULL,
  goals TEXT NOT NULL,
  available_days INTEGER NOT NULL,
  equipment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Unique user identifier
- `name`: User's full name
- `age`: User's age
- `fitness_level`: beginner, intermediate, advanced
- `goals`: User's fitness goals
- `available_days`: Days per week available for training
- `equipment`: Available equipment
- `created_at`: Account creation timestamp

### Workouts Table
```sql
CREATE TABLE workouts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  plan TEXT NOT NULL,
  nutrition_tips TEXT,
  feedback_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Fields:**
- `id`: Unique workout plan identifier
- `user_id`: Reference to user
- `plan`: Generated 7-day workout plan
- `nutrition_tips`: AI-generated nutrition recommendations
- `feedback_count`: Number of times plan was updated
- `created_at`: Plan generation timestamp

### Feedback Table
```sql
CREATE TABLE feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workout_id INTEGER NOT NULL,
  original_plan_id INTEGER NOT NULL,
  feedback TEXT NOT NULL,
  updated_plan TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (workout_id) REFERENCES workouts(id),
  FOREIGN KEY (original_plan_id) REFERENCES workouts(id)
);
```

**Fields:**
- `id`: Unique feedback record identifier
- `workout_id`: Current workout being updated
- `original_plan_id`: Reference to original plan
- `feedback`: User's feedback text
- `updated_plan`: Regenerated plan based on feedback
- `created_at`: Feedback submission timestamp

---

## Features

### 1. Personalized Workout Generation

The system generates customized 7-day workout plans based on:
- User's fitness level (beginner, intermediate, advanced)
- Fitness goals (muscle gain, weight loss, endurance)
- Available training days per week
- Available equipment
- User's age

**Generated Plan Includes:**
- Daily workout split
- Exercise recommendations
- Set and rep ranges
- Rest day suggestions
- Recovery tips

### 2. Nutrition & Recovery Recommendations

Based on user profile and fitness goals:
- Daily macronutrient requirements
- Meal timing suggestions
- Hydration guidelines
- Supplement recommendations
- Recovery protocols

### 3. Feedback-Based Regeneration

Users can provide feedback on their plan:
- "Too intense" → Easier, more accessible workouts
- "Not enough variety" → Different exercise combinations
- "Need more cardio" → Increased cardio sessions
- Original plan preserved for comparison

### 4. User Management

Store and manage user profiles:
- Multiple users support
- Profile modification
- Plan history tracking
- Feedback history

### 5. Admin Dashboard

Protected admin interface for:
- Viewing all registered users
- Reviewing user profiles
- Accessing all workout plans
- Tracking plan updates
- User statistics

### 6. API-First Architecture

Full REST API with:
- Swagger/OpenAPI documentation
- Structured request/response schemas
- Error handling
- Validation

---

## Usage Guide

### For End Users

#### 1. Create a Fitness Profile

1. Navigate to http://127.0.0.1:8000
2. Fill out the form:
   - Name
   - Age
   - Fitness Level
   - Fitness Goals
   - Days Available per Week
   - Available Equipment
3. Click "Generate My Plan"

#### 2. View Your Workout Plan

After generation, you'll see:
- 7-day workout breakdown
- Exercise details
- Nutrition recommendations
- Recovery tips

#### 3. Update Plan Based on Feedback

If unhappy with your plan:
1. Provide feedback (e.g., "Too intense")
2. Click "Regenerate Plan"
3. Review the updated plan
4. Compare with original if needed

#### 4. Track Plan History

Access your previous plans and their iterations through the dashboard.

### For Developers

#### Generate Plans Programmatically

```python
import requests

payload = {
    "name": "Jane Smith",
    "age": 25,
    "fitness_level": "intermediate",
    "goals": "improve flexibility and core strength",
    "available_days": 4,
    "equipment": "yoga mat, resistance bands"
}

response = requests.post(
    "http://127.0.0.1:8000/api/generate-plan",
    json=payload
)

plan = response.json()
print(plan["plan"])
```

#### Authenticate Admin Access

```python
from base64 import b64encode

username = "admin"
password = "change-me"
credentials = b64encode(f"{username}:{password}".encode()).decode()

headers = {
    "Authorization": f"Basic {credentials}"
}

response = requests.get(
    "http://127.0.0.1:8000/api/admin/users",
    headers=headers
)

users = response.json()
```

#### Access Swagger Documentation

Interactive API documentation available at:
```
http://127.0.0.1:8000/docs
```

Try out endpoints directly in the browser.

---

## Testing

### Run All Tests
```bash
pytest -q
```

**Expected Output:**
```
7 passed in 0.67s
```

### Run Specific Test
```bash
pytest tests/test_app.py::test_health_check -v
```

### Test with Mock AI (No API Key Required)

Set in `.env`:
```env
USE_MOCK_AI=true
```

Then run:
```bash
pytest
```

Tests use deterministic mock responses without consuming API quota.

### Test Coverage

```bash
pytest --cov=app --cov-report=html
```

View coverage report in `htmlcov/index.html`

### Manual Testing Checklist

- [ ] Form submission creates user
- [ ] Workout plan generates successfully
- [ ] Plan displays with proper formatting
- [ ] Feedback regeneration works
- [ ] Admin dashboard shows all users
- [ ] Admin auth fails with wrong credentials
- [ ] Database persists data after restart
- [ ] API returns correct status codes

---

## Deployment

### Docker Deployment

#### Build Docker Image
```bash
docker build -t fitbuddy:latest .
```

#### Run Container
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_api_key \
  -e ADMIN_PASSWORD=secure_password \
  fitbuddy:latest
```

#### Docker Compose
```yaml
version: '3.8'
services:
  fitbuddy:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=${ADMIN_PASSWORD}
      - DATABASE_URL=sqlite:///./fitbuddy.db
    volumes:
      - ./data:/app/data
```

Run with:
```bash
docker-compose up
```

### Cloud Deployment

#### Heroku Deployment

1. Create Procfile:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
heroku create fitbuddy-app
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

#### AWS EC2 Deployment

1. SSH into instance
2. Clone repository
3. Install Python and dependencies
4. Run with Gunicorn:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

#### Google Cloud Run

1. Push to Docker registry
2. Deploy:
```bash
gcloud run deploy fitbuddy \
  --image gcr.io/your-project/fitbuddy \
  --set-env-vars GEMINI_API_KEY=your_api_key
```

### Security Recommendations

- [ ] Change default admin password
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS in production
- [ ] Set strong CORS policies
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Log security events
- [ ] Regular dependency updates

---

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

#### Issue: "GEMINI_API_KEY not found"
**Solution:** Create and configure `.env` file
```bash
cp .env.example .env
# Add your API key to .env
```

#### Issue: "Address already in use: 0.0.0.0:8000"
**Solution:** Use different port
```bash
uvicorn app.main:app --reload --port 8001
```

#### Issue: Database lock error
**Solution:** Remove old database and recreate
```bash
rm fitbuddy.db
# Run application to recreate
uvicorn app.main:app --reload
```

#### Issue: Slow response from Gemini API
**Solution:** Check Gemini API status or use mock mode
```env
USE_MOCK_AI=true
```

#### Issue: Admin dashboard returns 401
**Solution:** Verify credentials in `.env`
```bash
# Check ADMIN_USERNAME and ADMIN_PASSWORD
cat .env | grep ADMIN
```

### Debug Mode

Enable verbose logging:
```env
DEBUG=true
```

Check logs while running:
```bash
uvicorn app.main:app --reload --log-level debug
```

### Performance Optimization

1. **Implement caching** for frequently accessed plans
2. **Use connection pooling** for database
3. **Add async operations** for API calls
4. **Implement pagination** for user listing
5. **Compress static files**

### Monitoring

Track:
- Response times
- Error rates
- API usage
- Database performance
- Gemini API quota

---

## Development Guide

### Adding New Features

#### 1. Add Database Model

In `app/models.py`:
```python
class NewFeature(Base):
    __tablename__ = "new_features"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # Add columns
```

#### 2. Add API Endpoint

In `app/routes.py`:
```python
@router.post("/new-feature")
async def create_feature(data: FeatureSchema):
    # Implementation
    return result
```

#### 3. Add Test

In `tests/test_app.py`:
```python
def test_new_feature():
    response = client.post("/api/new-feature", json=test_data)
    assert response.status_code == 200
```

### Code Style

Follow PEP 8:
```bash
pip install black flake8
black app/
flake8 app/
```

### Git Workflow

```bash
git checkout -b feature/new-feature
# Make changes
git commit -m "Add new feature"
git push origin feature/new-feature
# Create pull request
```

---

## Support & Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [Google Gemini API](https://ai.google.dev)
- [Jinja2 Templates](https://jinja.palletsprojects.com)

### Getting Help

1. Check troubleshooting section
2. Review application logs
3. Check API documentation at `/docs`
4. Review test cases for usage examples

### Version Info
- FastAPI: ^0.95.0
- SQLAlchemy: ^2.0.0
- google-generativeai: ^0.3.0
- Python: ^3.8

---

## License

This project is provided as-is for educational and development purposes.

## Changelog

### Version 1.0.0 (Initial Release)
- Core workout generation
- Nutrition recommendations
- Feedback-based regeneration
- Admin dashboard
- API endpoints
- Docker support
- Test suite

---

**Last Updated:** January 2024
**Project Status:** Active Development
**Support:** Documentation and inline code comments
