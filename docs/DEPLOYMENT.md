# 🚀 Deployment Guide | CUTM AI-Enabled University Portal

This document provides step-by-step instructions on how to publish (deploy) this full-stack Python Flask + SQLite + HTML/CSS/JS website to the internet for free.

---

## 🌟 Method 1: Deploy on Render.com (Recommended - 100% Free & Easiest)

Render is one of the most reliable modern cloud platforms with a generous free tier, automatic SSL certificate (HTTPS), and zero server management.

### Step 1: Upload Project to GitHub
1. Create a free account at [github.com](https://github.com).
2. Create a new repository named `cutm-ai-portal` (make it Public or Private).
3. Push your project code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of CUTM portal"
   git branch -M main
   git remote add origin https://github.com/<your-username>/cutm-ai-portal.git
   git push -u origin main
   ```

### Step 2: Create a Web Service on Render
1. Open [dashboard.render.com](https://dashboard.render.com/) and sign up with GitHub.
2. Click **New +** > **Web Service**.
3. Select your GitHub repository (`cutm-ai-portal`) and click **Connect**.
4. Configure the service settings:
   - **Name**: `cutm-portal` (or any name you choose)
   - **Region**: Singapore or Frankfurt (choose nearest)
   - **Branch**: `main`
   - **Root Directory**: *(leave blank)*
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn --chdir backend app:app
     ```
   - **Instance Type**: `Free`

### Step 3: Add Environment Variables (Optional)
Under the **Environment Variables** section:
- `JWT_SECRET`: `cutm_production_secret_key_2026`
- `ADMIN_USERNAME`: `admin`
- `ADMIN_PASSWORD`: `YourStrongAdminPassword`

### Step 4: Click "Create Web Service"
- Render will build the virtual environment, install packages, and launch Gunicorn.
- Within 2-3 minutes, your live site will be live at:
  **`https://cutm-portal.onrender.com`**

---

## 🐍 Method 2: Deploy on PythonAnywhere (100% Free & Built for Python)

PythonAnywhere is specifically designed for Python & Flask applications and retains your SQLite database cleanly.

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com/) and create a free Beginner account.
2. Your username will be part of your website URL: `https://<username>.pythonanywhere.com`.

### Step 2: Upload Files
1. Open the **Bash Console** on PythonAnywhere.
2. Clone your GitHub repository or upload your project zip:
   ```bash
   git clone https://github.com/<your-username>/cutm-ai-portal.git
   ```

### Step 3: Set up Virtual Environment
In the Bash console:
```bash
mkvirtualenv --python=/usr/bin/python3.10 cutm-venv
pip install -r cutm-ai-portal/requirements.txt
```

### Step 4: Configure Web App
1. Go to the **Web** tab in PythonAnywhere dashboard.
2. Click **Add a new web app** > Select **Flask** (or Manual configuration) > **Python 3.10**.
3. In **Virtualenv**, enter: `/home/<username>/.virtualenvs/cutm-venv`.
4. In **Source code**, enter: `/home/<username>/cutm-ai-portal`.
5. Click on the **WSGI configuration file** link and set it to:
   ```python
   import sys
   import os

   path = '/home/<username>/cutm-ai-portal/backend'
   if path not in sys.path:
       sys.path.insert(0, path)

   from app import app as application
   ```
6. Click **Save**, return to the Web tab, and click the green **Reload <username>.pythonanywhere.com** button.
7. Your website is instantly live at: **`https://<username>.pythonanywhere.com`**!

---

## 🚂 Method 3: Deploy on Railway.app

1. Go to [railway.app](https://railway.app/) and sign in with GitHub.
2. Click **New Project** > **Deploy from GitHub repo**.
3. Select `cutm-ai-portal`.
4. Railway will automatically detect Python and the root `Procfile`:
   `web: gunicorn --chdir backend app:app`
5. Click **Generate Domain** in service settings to get a public URL.

---

## 🔒 Post-Deployment Checklist

1. **Verify Home Page**: Open your live URL in a browser and check if the CUTM logo, hero image, and navbar load.
2. **Test Application Submission**: Go to `/admissions`, fill a test student form, and verify that the `CUTM-XXXXXX` reference code is generated.
3. **Test Admin Console**: Navigate to `/login`, sign in with `admin` credentials, and check that `/dashboard` opens and receives live leads.
4. **Change Default Password**: Ensure you change `admin1234` in production via environment variables.

