# AI University Events Website

## Run locally on Windows

1. Install Python dependencies into the project virtual environment:

   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. Run `run.bat`. The backend creates a local SQLite database automatically and opens the website at `http://127.0.0.1:5000/`.
3. Open `http://127.0.0.1:5000/login` to manage events and registrations. The local-only starter login is `admin` / `admin1234`.
4. For a private deployment, copy `.env.example` to `.env` and change `JWT_SECRET`, `ADMIN_USERNAME` and `ADMIN_PASSWORD`.
5. To enable generated AI answers, set `AI_API_KEY` in `.env`. The key stays on the backend; do not put it in frontend files. Without a key, the assistant uses its event FAQ replies.

The local database is stored in `backend\data\university.db` and is created on first run. Admins can create, edit and delete events from the dashboard; event registrations and course enquiries are stored locally and shown in the admin dashboard. Built-in sample events are inserted only on the first run.

## AI provider configuration

The assistant uses the OpenAI-compatible chat completions API. Set `AI_API_URL` and `AI_MODEL` to use a compatible provider. If the key is absent, the website continues to use the built-in event FAQ assistant.

The app binds to `127.0.0.1` for local development. Do not expose the starter admin credentials or development server directly to the public internet.
