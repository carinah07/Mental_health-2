# PAWHA Mental Health

Public mental-health web app with a Django REST backend and Vue frontend.

## Structure

```text
backend/   Django API, feature apps, settings, and requirements
frontend/  Public Vue/Vite app
```

The custom admin backend app and admin Vue panel have been removed. Public API routes remain under `/api/chatbot/`, `/api/assessment/`, `/api/education/`, and `/api/experts/`.

## Development

```sh
cd backend
python manage.py runserver
```

```sh
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` for the frontend if the API is not running at `http://127.0.0.1:8000`.
