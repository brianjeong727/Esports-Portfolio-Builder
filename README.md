<<<<<<< HEAD
# Esports Portfolio Builder (minimal scaffold)

This repository contains a minimal Django backend and a Vite React frontend scaffold for an "Esports Portfolio Builder" demo.

Backend (Django):

- Python virtualenv is included in `env/` (optional). Activate it before running Django commands.
- Install requirements (if you don't use the provided env):

  python -m venv env
  source env/bin/activate
  pip install django djangorestframework django-cors-headers

- Run migrations and start server:

  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver

The API endpoints are available at `http://127.0.0.1:8000/api/profiles/`.

## Riot API proxy

Set your Riot API key in the environment before starting the Django server:

```bash
export RIOT_API_KEY=your_riot_api_key_here
```

Available proxy endpoints (server-side, require key):

- `/api/riot/lol/<region>/summoner/by-name/<name>/`
- `/api/riot/tft/<region>/summoner/by-name/<name>/`
- `/api/riot/valorant/<region>/account/by-puuid/<puuid>/`

You can use the frontend Lookup page at `/lookup` to try them.

Frontend (Vite + React):

- From the `frontend/` directory:

  npm install
  npm run dev

By default the frontend will POST to `http://127.0.0.1:8000/api/profiles/`. If your backend is running on a different host, set `VITE_API_BASE` in an `.env` file inside `frontend/`.
=======
# Esports-Portfolio-Builder
In progress...
>>>>>>> 7cd374c1a061fb65d103a80873333bae65e228f8
