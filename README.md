# MindCare Mental Health

Public mental-health web app with a Django REST backend and Vue frontend.

## Structure

```text
backend/   Django API, feature apps, settings, and requirements
frontend/  Public Vue/Vite app
```

Education and Experts modules have been removed; all enquiries are now handled by the chatbot at `/api/chatbot/`. Public API routes remain under `/api/assessment/` and `/api/chatbot/`.

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
