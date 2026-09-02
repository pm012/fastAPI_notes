# fastAPI_notes

FastAPI app

## Instructions for installation poetry environment

1. Ensure you have installed **pyenv** and active Python version (for example, 3.14.0).
2. Install poetry **Poetry** (if you haven't installed it yet):
   ```bash
   sudo apt install pipx && pipx install poetry
   ```
3. Enable creating virtual environment in the folder of the project:
   ```bash
   poetry config virtualenvs.in-project true
   ```
4. Install all the dependencies in the project:
   ```bash
   poetry install
   ```
5. launch the project:
   TBD!!!!!!!!!!!!!
   Запуск бази даних

   ```bash
   docker compose -up -d
   ```

   ```bash
   poetry run uvicorn src.main:app --reload
   ```
