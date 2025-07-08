# ⏱️ Time It Right – FastAPI Developer Challenge

A precision-based timer game API built with **FastAPI**, where players try to stop a timer as close as possible to 10 seconds. This challenge demonstrates clean backend architecture, test coverage, API validation, and deployment to the cloud.

---

## 🚀 Live API Documentation

**Documentation is available at:**

🔗 [https://time-it-right-back.onrender.com/docs](https://time-it-right-back.onrender.com/docs)

> ⚠️ Endpoints are **not active** in the live environment due to Render’s limitations on database migrations and CLI access for free-tier PostgreSQL.

---

## 📁 Project Structure

```
.
├── app/                    # FastAPI app (routes, models, services)
├── scripts/                # Shell utilities: dev, tests, db
│   ├── dev.sh              # One-command local run (Docker + migrations)
│   └── run_tests.sh        # Runs all tests and logs to /logs
├── tests/                  # Pytest unit and integration tests
├── postman/                # Postman collection with full test coverage
├── logs/                   # Stores test execution logs
├── alembic/                # Database migrations
├── Dockerfile              # Docker setup
├── docker-compose.yml      # Compose for DB & app
├── requirements.txt
└── README.md
```

---

## 🧪 Features Implemented

✅ JWT Authentication (Register, Login, Current User)  
✅ Start/Stop game sessions (tracks duration and deviation)  
✅ Expiration of sessions after 30 minutes  
✅ Deviation calculation from 10,000ms (target)  
✅ Leaderboard (avg/best deviation, paginated)  
✅ Individual user analytics  
✅ Custom error handling with exceptions  
✅ Full test coverage (routes, services)  
✅ Alembic migrations with PostgreSQL  
✅ Postman collection with test scripts  
✅ Dockerized environment for dev & deploy  
✅ Deployed on Render with auto-build from GitHub  

---

## 💻 Local Development

### 1. Prerequisites

- Docker + Docker Compose
- Python 3.11 (for local dev/test outside Docker)
- Git

### 2. Start the app locally

From the root of the project:

```bash
cd scripts
./dev.sh
```

This script will:
- Build Docker containers
- Start FastAPI app at `http://localhost:8000`
- Run Alembic migrations automatically (if needed)

You can now access:
- API: [http://localhost:8000](http://localhost:8000)
- Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Run tests

```bash
cd scripts
./run_tests.sh
```

This runs `pytest` and stores logs in `logs/` for inspection.

---

## 📊 Leaderboard Logic

- **Target**: 10,000 milliseconds (10 seconds)
- **Deviation**: `abs(duration_ms - 10_000)`
- **Rank Criteria**:
  - Average deviation (ascending)
  - Best deviation
  - Number of total games
- Pagination supported via `page` and `limit`

---

## 🔐 Authentication

All protected routes require a Bearer token (JWT). Use the `/auth/login` endpoint to obtain one after registration.

---

## 🧪 Postman Collection

The collection is in `/postman/time_it_right_complete.postman_collection.json` and includes:

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me` *(Requires token)*

### Game Mechanics

- `POST /games/start` *(Requires token)*
- `POST /games/{session_id}/stop` *(Requires token)*

### Leaderboard & Analytics

- `GET /games/leaderboard?page=1&limit=10`
- `GET /games/analytics/{user_id}` *(Requires token)*

### Edge Cases

- Invalid session stop
- Missing/invalid token handling

All requests include Postman test scripts and environment variables for `{{token}}`, `{{user_id}}`, etc.

---

## 🌐 Deployment on Render

The project is deployed on [Render](https://render.com):

- Web Service uses **Docker environment**
- PostgreSQL hosted on Render as well
- Environment variables (`DATABASE_URL`, `SECRET_KEY`, etc.) are configured in the dashboard

**Note:** The live endpoints are disabled for now due to database console limitations on free tier.

---

## 🛠 Tech Stack

- **FastAPI** with dependency injection
- **PostgreSQL** via SQLAlchemy async + Alembic
- **Docker & Compose**
- **Pytest** for unit & integration tests
- **Pydantic** for validation
- **JWT** for auth (with token expiration)
- **Render** for deployment
- **Postman** for API testing

---

## 📌 Considerations

- All project commands are automated via `scripts/`
- Tests are separated and logged for CI integration
- Uses async best practices throughout services and DB layer
- Custom exceptions improve error clarity for API consumers
- Future extensions could include WebSocket support or multi-user sessions

---

## ✅ Challenge Compliance

- [x] All core features implemented (auth, game, leaderboard, analytics)
- [x] JWT auth with protected endpoints
- [x] PostgreSQL + async SQLAlchemy + Alembic
- [x] Full test coverage with Pytest
- [x] Postman collection with edge cases
- [x] Docker-ready with simple startup script
- [x] Hosted API documentation online (Render)
- [x] Clean, modular code following SOLID principles

---

## 📬 Contact

Made with 😄 [Aram Kechichian](https://www.linkedin.com/in/aramkechichian/)


---

### 🧪 Test Data Endpoint

To facilitate local testing and leaderboard simulation, a dedicated developer endpoint is available:

```
POST http://localhost:8000/games/dev/load-test-data
```

This endpoint will populate the database with sample users and game sessions for testing purposes.  
It is only available in the development environment and should not be exposed in production.

Use it to quickly seed realistic data for:

- Leaderboard evaluation
- User analytics endpoints
- Manual UI testing via Postman or Swagger
