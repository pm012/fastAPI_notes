# fastAPI_notes

FastAPI application for managing personal notes and tags with a fully asynchronous architecture.

## Local Deployment Instructions

### 1. Environment and Tools Setup

- Ensure you have installed **pyenv** and have an active Python version (for example, **3.14.0**).
- Install **Poetry** via `pipx` (if you haven't installed it yet):
  ```bash
  sudo apt install pipx && pipx install poetry
  ```
- Configure Poetry to create the virtual environment inside the project directory:
  ```bash
  poetry config virtualenvs.in-project true
  ```

### 2. Installation

- Install all the required dependencies using Poetry:
  ```bash
  poetry install
  ```
- Create a `.env` file in the root of the project and populate it with your local configuration:
  ```env
  POSTGRES_DB=rest_app
  POSTGRES_USER=serhii
  POSTGRES_PASSWORD=secret01
  POSTGRES_HOST=localhost
  POSTGRES_PORT=5432
  ```

### 3. Database Initialization

- Launch the PostgreSQL database container inside Docker:
  ```bash
  sudo docker compose up -d
  ```
- Run database migrations via Alembic to create the required tables:
  ```bash
  poetry run alembic upgrade head
  ```

### 4. Running the Application

- Launch the FastAPI development server using Uvicorn:
  ```bash
  poetry run uvicorn main:app --reload
  ```
- Open your browser and navigate to the interactive Swagger documentation to test the endpoints:
  [http://127.0.0.1:8000/docs#](http://127.0.0.1:8000/docs#)
