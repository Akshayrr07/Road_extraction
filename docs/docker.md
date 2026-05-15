# docs/docker.md

# 🐳 Docker & Development Setup

## Backend Dockerfile

Create:

```text
backend/Dockerfile
```

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--workers", "1", "--threads", "1", "app.app:app", "--bind", "0.0.0.0:5000"]
```

---

## Frontend Dockerfile

Create:

```text
frontend/Dockerfile
```

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
```

---

## Docker Compose

Create:

```text
docker-compose.yml
```

```yaml
version: '3.9'

services:

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

---

## Run Full Stack

```bash
docker compose up --build
```

## Clone Repository

```bash
git clone https://github.com/Akshayrr07/Road_extraction.git

cd Road_extraction
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python app/app.py
```

Backend runs at:

```text
http://127.0.0.1:5000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Frontend Environment Variables

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_URL=https://road-extraction-api.onrender.com
```

---

## Branch Workflow

| Branch          | Purpose                                   |
| --------------- | ----------------------------------------- |
| main            | Stable production deployment              |
| ui-dev          | Frontend and UI development               |
| ml-optimization | AI model optimization and experimentation |

---

## Important Rules

* Never push experimental code directly to `main`
* Use pull requests before merging
* Test frontend and backend before pushing
* Keep deployment-safe code inside `main`

---

## Clone Repository

```bash
git clone https://github.com/Akshayrr07/Road_extraction.git
```

---

## Switch Branch

### UI Development

```bash
git checkout ui-dev
```

### ML Development

```bash
git checkout ml-optimization
```

---

## Push Changes

```bash
git add .

git commit -m "your message"

git push
```
