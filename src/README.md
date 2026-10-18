# 📦 CUTM Modular Source (`src/`)

This directory contains the modular, factory-pattern implementation of the CUTM AI-Enabled University platform.

## Architecture
- `app.py`: Flask application factory pattern (`create_app()`).
- `config.py`: Central environment configurations, directory paths, and course/event definitions.
- `database.py`: SQLite connection handling and table persistence functions.
- `auth.py`: JWT token encoding, decoding, and route security decorators.
- `scoring.py`: AI composite scoring and predictive admission algorithms.

This modular structure allows for automated unit testing and scalable extensions alongside the root WSGI application.

