# STANDARD.IO - Free Deployment Guide

## 🎯 Recommended: Railway (Backend) + Vercel (Frontend)

**Cost: $0/month forever | No credit card required | No sleep on free tier**

---

## 📋 Prerequisites

1. GitHub account
2. Code pushed to GitHub repository
3. Vercel account (free)
4. Railway account (free, login with GitHub)

---

## 🚂 Step 1: Deploy Backend to Railway

### 1.1 Prepare Repository

Your repo structure should be:
```
your-repo/
├── backend/          # ← Railway will use this folder
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── railway.json
│   ├── .env.example
│   └── ...
├── frontend/
├── railway.json      # Root config (optional)
├── render.yaml       # Alternative
├── Dockerfile        # Alternative
└── DEPLOYMENT.md
```

### 1.2 Deploy on Railway

1. Go to **[railway.app](https://railway.app)** → "Login with GitHub"
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. **Important**: Set **Root Directory** to `backend/`
5. Click **"Deploy Now"**

### 1.3 Add PostgreSQL Database (Free)

1. In your Railway project dashboard, click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway automatically adds `DATABASE_URL` environment variable
3. Wait for deployment to complete (2-3 minutes)

### 1.4 Set Environment Variables

In Railway dashboard → **Variables** tab, add:

| Variable | Value |
|----------|-------|
| `CORS_ORIGINS` | `https://your-vercel-app.vercel.app` (add after Vercel deploy) |
| `SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_EXPIRE_MINUTES` | `1440` |

### 1.5 Get Your API URL

After deployment, Railway gives you: `https://your-app-name.up.railway.app`

**Test endpoints:**
- `https://your-app.up.railway.app/docs` → Swagger UI
- `https://your-app.up.railway.app/health` → Health check
- `https://your-app.up.railway.app/api/products` → Products API

---

## 🔺 Step 2: Deploy Frontend to Vercel

### 2.1 Prepare Frontend Config

Your `frontend/` folder already has:
- `vercel.json` (configured)
- `.env.example` (copy to `.env.local` for local dev)

### 2.2 Deploy on Vercel

1. Go to **[vercel.com](https://vercel.com)** → "Add New..." → "Project"
2. Import your GitHub repository
3. **Configure:**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### 2.3 Set Environment Variables

In Vercel project settings → **Environment Variables**, add:

| Name | Value | Environment |
|------|-------|-------------|
| `VITE_API_BASE_URL` | `https://your-railway-app.up.railway.app/api` | Production |
| `VITE_API_BASE_URL` | `http://localhost:8000/api` | Development (optional) |

### 2.4 Deploy

Click **"Deploy"** → Wait 1-2 minutes → Your app: `https://your-app.vercel.app`

---

## 🔗 Step 3: Connect Frontend ↔ Backend

### 3.1 Update Railway CORS

In Railway → Variables, update `CORS_ORIGINS`:

```
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

### 3.2 Redeploy Backend

Railway auto-redeploys when env vars change. Or click **"Deploy"** manually.

---

## ✅ Step 4: Verify Everything Works

| Test | URL | Expected |
|------|-----|----------|
| Frontend | `https://your-app.vercel.app` | Storefront loads |
| Login | `https://your-app.vercel.app/login` | Login page works |
| Customer Login | `user@standard.io` / `user123` | Redirects to `/shop` |
| Admin Login | `admin@standard.io` / `admin123` | Redirects to `/admin` |
| API Health | `https://your-railway.up.railway.app/health` | `{"status":"healthy"}` |
| API Docs | `https://your-railway.up.railway.app/docs` | Swagger UI |
| Products API | `https://your-railway.up.railway.app/api/products` | JSON array |

---

## 🐳 Alternative: Render (All-in-One)

If you prefer single-platform deployment:

### 1. Push `render.yaml` to repo root (already created)

### 2. Deploy on Render

1. Go to **[render.com](https://render.com)** → "New" → "Blueprint"
2. Connect GitHub repo
3. Render creates:
   - `standard-io-api` (Python web service)
   - `standard-io-frontend` (Static site)
   - `standard-io-db` (PostgreSQL database)
4. Click **"Apply"**

### 3. Note on Render Free Tier

- Services **sleep after 15 min inactivity**
- First request after sleep takes ~30 seconds (cold start)
- Add `autoDeploy: true` in render.yaml for auto-deploys

---

## 🐳 Alternative: Fly.io (Docker)

### 1. Install flyctl

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Or download from https://fly.io/docs/hands-on/install-flyctl/
```

### 2. Deploy

```bash
cd your-repo
fly auth login
fly launch --no-deploy  # Creates fly.toml
fly postgres create --name standard-io-db --region iad --plan hobby
fly deploy
```

---

## 🔧 Local Development with Production Config

### Backend

```bash
cd backend
cp .env.example .env
# Edit .env with your local values
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
# Edit .env.local: VITE_API_BASE_URL=http://localhost:8000/api
npm run dev
```

---

## 🔐 Generate Secret Key

```bash
# Option 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 2: OpenSSL
openssl rand -base64 32

# Option 3: Node
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

---

## 📝 Environment Variables Summary

### Railway (Backend)
```env
DATABASE_URL=postgresql://...  # Auto-set by Railway
CORS_ORIGINS=https://your-app.vercel.app
SECRET_KEY=your-generated-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

### Vercel (Frontend)
```env
VITE_API_BASE_URL=https://your-railway-app.up.railway.app/api
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Check `CORS_ORIGINS` in Railway matches Vercel URL exactly |
| API 404 | Ensure `VITE_API_BASE_URL` ends with `/api` |
| DB connection failed | Verify PostgreSQL added in Railway; check `DATABASE_URL` |
| Build fails | Check Node version (use 22.x); clear Vercel cache |
| Static files not served | Ensure `StaticFiles` mount in `main.py` points to `./static` |
| Auth redirect loop | Check `withCredentials: true` in axios config |

---

## 🔄 CI/CD (Optional)

Add GitHub Actions for auto-deploy:

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: railway-app/railway-deploy@v1
        with:
          token: ${{ secrets.RAILWAY_TOKEN }}
          service: standard-io-api

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
```

---

## ✅ Final Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created with `backend/` as root
- [ ] PostgreSQL database added on Railway
- [ ] `CORS_ORIGINS` set to Vercel URL
- [ ] `SECRET_KEY` generated and set
- [ ] Vercel project created with `frontend/` as root
- [ ] `VITE_API_BASE_URL` set to Railway URL + `/api`
- [ ] Both deployments successful
- [ ] Customer login works (`user@standard.io` / `user123`)
- [ ] Admin login works (`admin@standard.io` / `admin123`)
- [ ] Cart, wishlist, checkout, orders all functional
- [ ] Admin dashboard shows analytics, inventory, orders

---

**🎉 Done! Your STANDARD.IO is live for free!**