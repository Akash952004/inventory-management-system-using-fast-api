# Akash Inventory Manager

A full-stack product inventory app with a React frontend, FastAPI REST API, and PostgreSQL database.

## Backend

Install the Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Set the connection string for your PostgreSQL database and start the API. Add your local database credentials to the environment variable if your PostgreSQL setup requires them; do not commit those credentials.

```powershell
$env:DATABASE_URL = "postgresql://localhost:5432/fastapi_project"
python -m uvicorn main:app --reload
```

The API is available at `http://localhost:8000`. Interactive API documentation is at `http://localhost:8000/docs`.

## Frontend

In a separate terminal:

```powershell
cd frontend
npm ci
npm start
```

The frontend is available at `http://localhost:3000`.
