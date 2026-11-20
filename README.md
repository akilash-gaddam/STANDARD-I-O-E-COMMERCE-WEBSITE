# STANDARD.IO — Urban Grocer E-Commerce Platform

A full-stack supermarket e-commerce platform built with **React + Vite + Tailwind CSS** (frontend) and **FastAPI + SQLAlchemy + SQLite/PostgreSQL** (backend).

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 22+
- Git

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/standard-io.git
cd standard-io

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Demo Credentials
| Role | Email | Password |
|------|-------|----------|
| Customer | user@standard.io | user123 |
| Admin | admin@standard.io | admin123 |

---

## 🏗 Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React SPA     │────▶│   FastAPI       │────▶│   SQLite/       │
│   (Vite)        │     │   (REST + JWT)  │     │   PostgreSQL    │
│   Port 5173     │     │   Port 8000     │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## ✨ Features

### Customer Portal
- 🛍 Product catalog with search & category filters
- 🛒 Shopping cart with quantity controls
- ❤️ Wishlist with move-to-cart
- 📦 Address book management
- 💳 Checkout flow
- 📋 Order history with 4-stage tracking (Placed → Packed → Out for Delivery → Delivered)

### Admin Console
- 📊 Analytics dashboard (Revenue, Profit, Margin, Charts)
- 📦 Inventory management (CRUD, stock steppers)
- 🚚 Order dispatch board (Status updater)
- 🔍 Low-stock alerts

### Technical
- 🔐 JWT authentication with role-based access
- 🎨 Luxury dark-mode UI (Tailwind CSS)
- 🖼 Product images with SVG fallbacks
- ✅ 33 automated tests (100% passing)

---

## 🌐 Free Deployment

### Recommended: Railway (Backend) + Vercel (Frontend)

| Platform | Service | Free Tier |
|----------|---------|-----------|
| **Railway** | Backend + PostgreSQL | 500 hrs/mo, no sleep |
| **Vercel** | Frontend | Unlimited |

**Deploy in 5 minutes:** See [DEPLOYMENT.md](DEPLOYMENT.md)

### Alternatives
- **Render**: All-in-one (sleeps after 15 min inactivity)
- **Fly.io**: Docker-based (3 free VMs, 160 GB bandwidth)
- **Docker**: Single container deployment

---

## 📁 Project Structure

```
standard-io/
├── backend/
│   ├── main.py              # FastAPI app, CORS, static files
│   ├── database.py          # SQLAlchemy engine (SQLite/PostgreSQL)
│   ├── models.py            # ORM models (User, Product, Order, etc.)
│   ├── seed.py              # 18 products across 5 categories
│   ├── deps.py              # Auth dependencies
│   ├── auth_utils.py        # Password hashing, JWT
│   ├── routers/
│   │   ├── auth.py          # Register, login, me
│   │   ├── products.py      # Public product listing
│   │   ├── customer.py      # Cart, wishlist, addresses, orders
│   │   └── admin.py         # Inventory, dispatch, analytics
│   ├── tests/
│   │   └── test_standard_io.py  # 33 pytest tests
│   ├── requirements.txt
│   ├── railway.json
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── pages/           # Login, Shop, Checkout, Orders, Admin
│   │   ├── components/      # ProductCard, Drawers, Navbar, UI
│   │   ├── context/         # Auth, Cart, Wishlist providers
│   │   ├── api/             # Axios client with JWT interceptor
│   │   └── utils/           # Helpers
│   ├── vercel.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── .env.example
│   └── package.json
├── railway.json             # Railway config
├── render.yaml              # Render Blueprint
├── Dockerfile               # Multi-stage Docker build
├── fly.toml                 # Fly.io config
├── DEPLOYMENT.md            # Detailed deployment guide
├── .github/workflows/       # CI/CD pipelines
└── README.md
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/test_standard_io.py -v
# Expected: 33 passed

# Frontend lint
cd frontend
npm run lint
```

---

## 🔧 Configuration

### Backend Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL or SQLite URL | Auto on Railway/Render |
| `CORS_ORIGINS` | Comma-separated allowed origins | Yes (prod) |
| `SECRET_KEY` | JWT signing key | Yes (prod) |
| `JWT_ALGORITHM` | JWT algorithm (HS256) | Default |
| `JWT_EXPIRE_MINUTES` | Token expiry (1440 = 24h) | Default |

### Frontend Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_BASE_URL` | Backend API URL | Yes (prod) |

---

## 📚 API Documentation

Interactive docs at `/docs` (Swagger UI) when backend is running.

### Key Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | No | Register user |
| POST | `/api/auth/login` | No | Login, get JWT |
| GET | `/api/products` | No | List products |
| GET | `/api/customer/cart` | Customer | Get cart |
| POST | `/api/customer/orders` | Customer | Place order |
| GET | `/api/customer/orders` | Customer | Order history |
| GET | `/api/admin/analytics` | Admin | Business metrics |
| GET | `/api/admin/products` | Admin | Manage inventory |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **React** - Component library
- **Tailwind CSS** - Utility-first CSS
- **Recharts** - Data visualization
- **Lucide React** - Beautiful icons
- **SQLAlchemy** - Python ORM
- **Railway/Vercel** - Free hosting

---

**Built with ❤️ for SOFTWARE ENGINEERING AND SYSTEM DESIGN (24CS301PC311)**  
**SR University, Warangal, Telangana, India (2026-2027)**