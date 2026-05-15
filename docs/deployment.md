# docs/deployment.md

# 🚀 Deployment Guide

## Backend Deployment (Render)

Platform:

* Render

### Backend Settings

| Setting        | Value                                        |
| -------------- | -------------------------------------------- |
| Root Directory | backend                                      |
| Environment    | Python                                       |
| Build Command  | pip install -r requirements.txt              |
| Start Command  | gunicorn --workers 1 --threads 1 app.app:app |

----

## Frontend Deployment (Vercel)

Platform:

* Vercel

### Frontend Settings

| Setting          | Value         |
| ---------------- | ------------- |
| Framework        | Vite          |
| Root Directory   | frontend      |
| Build Command    | npm run build |
| Output Directory | dist          |

----

## Production URLs

### Frontend

[https://road-extraction-livid.vercel.app/](https://road-extraction-livid.vercel.app/)

### Backend

[https://road-extraction-api.onrender.com](https://road-extraction-api.onrender.com)
