# 🏡 EstateHub - Enterprise Real Estate Property Listing Platform

EstateHub is a modern, high-fidelity full-stack real estate property listing and client-to-agent lead generation platform. Built with **FastAPI, React, PostgreSQL, Docker, and JWT Authentication**, it features a clean responsive interface with theme synchronization (Light/Dark mode) and premium micro-animations.

The application allows users to discover, search, and manage property listings through role-based guards. It handles user authentication, profile updates, rating/review systems, and interactive multi-photo uploads for listings.

---

# 📌 Table of Contents

- Features
- Tech Stack
- Project Structure
- API Documentation
- API Modules
- Database
- Useful Commands
- Future Improvements

---

# ✨ Features

## 🔐 User Authentication

- User Registration
- User Login
- JWT Authentication
- Access Token & Refresh Token
- Password Hashing
- Role-Based Authorization

### Supported Roles

- 👑 Admin
- 💼 Agent
- 👤 Buyer

---

## 🏡 Property Management

Users can:

- Create Property Listings
- View All Properties
- View Property Details
- Update Property Listings
- Delete Property Listings

Each property contains:

- Title
- Description
- Property Type
- Purpose (Sale/Rent)
- Price
- Area (sqft)
- Bedrooms
- Bathrooms
- Furnishing Status
- Parking Availability
- Property Images
- Amenities
- Country
- State
- City
- Address
- ZIP Code
- Agent Details

Property IDs are generated using UUID.

---

## 🔍 Property Search & Filtering

Users can search properties using:

- Property Type
- Price Range
- Location
- Bedrooms
- Bathrooms
- Furnishing Status

---

## ❤️ Favorites

Registered users can:

- Add Property to Favorites
- Remove Property from Favorites
- View Favorite Properties

---

## ⭐ Reviews & Ratings

Users can:

- Add Reviews
- Update Reviews
- Delete Reviews
- View Reviews

---

## 🏢 Amenities

Supports management of amenities such as:

- Air Conditioning
- Parking
- Garden
- Swimming Pool
- Gym
- Internet
- Security

---

## 🌍 Location Management

Supports management of:

- Countries
- States
- Cities

---

## 🔔 Notifications

Provides notification support for important user activities.

---

## 💻 Responsive Frontend

The React frontend includes:

- Home Page
- Login & Registration
- Property Listings
- Property Details
- Favorites
- User Dashboard
- Admin Dashboard
- Add/Edit Property
- Search & Filters
- Responsive UI

---

# 🛠️ Tech Stack

## Frontend (Single Page Application)
- **Framework & UI**: React 19, React DOM
- **Bundler & Tooling**: Vite 8, PostCSS, Autoprefixer, Oxlint
- **Routing**: React Router DOM 7
- **Styling**: Tailwind CSS v4 (with full Light/Dark mode responsiveness)
- **State Management**: Context API (Auth, Favorites, User, Notifications)
- **HTTP Client**: Axios (configured with request/response interceptors for JWT Bearer tokens and token refresh)
- **UX & Graphics**: Framer Motion, Recharts, Swiper, Lucide React
- **Utility**: Day.js, React Hook Form, Yup

## Backend (Async RESTful API)
- **Language**: Python 3.13
- **Framework**: FastAPI (conforming to OpenAPI and Swagger specifications)
- **Server**: Uvicorn
- **ORM & Database Connection**: SQLAlchemy 2.0 (using asyncio sessions and eager loading), AsyncPG
- **Migrations**: Alembic
- **Validation**: Pydantic v2, Pydantic Settings
- **Auth & Cryptography**: PyJWT, Passlib (bcrypt)
- **Middleware**: CORSMiddleware, custom AuthStateMiddleware, custom RequestLoggerMiddleware

## Database
- **Engine**: PostgreSQL (Docker containers)

## Tools

- Docker
- Docker Compose
- pgAdmin
- Postman
- Git
- GitHub
- VS Code


---

# 📡 API Modules

The backend provides REST APIs for:

- Authentication
- Users
- Properties
- Amenities
- Favorites
- Reviews
- Notifications
- Locations
- Admin

All APIs can be tested using:

- Swagger UI
- Postman

---

# 🗄️ Database

Database used:

- PostgreSQL

Database Management Tool:

- pgAdmin

Example connection:

| Field | Value |
|-------|-------|
| Host | localhost |
| Port | 5432 |
| Database | Your Database Name |
| Username | Your PostgreSQL Username |
| Password | Your PostgreSQL Password |

---

# 🧰 Useful Commands

### Start Docker

```bash
docker compose start
```

### Stop Docker

```bash
docker compose stop
```

### Check Running Containers

```bash
docker ps
```

### Reset Database

```bash
docker compose down -v
```

### Run Backend

```bash
python run.py
```

### Run Frontend

```bash
cd frontend
npm run dev
```

### Save Dependencies

```bash
pip freeze > requirements.txt
```

---

# 📁 Git Ignore

The project ignores:

- `.env`
- `.venv`
- `__pycache__/`
- `node_modules/`
- IDE settings
- Python cache files

Never commit environment variables or secrets to GitHub.

---

# 🚀 Future Improvements

- Google Maps Integration
- Property Recommendation System
- Email Notifications
- Property Analytics Dashboard
- Payment Integration
- Image Optimization
- Advanced Search Filters
- Cloud Deployment


---

# 📌 Summary

This project demonstrates a modern full-stack Real Estate Property Listing Application using:

- FastAPI
- React
- PostgreSQL
- Docker
- Async SQLAlchemy
- JWT Authentication
- REST APIs
- CRUD Operations
- Role-Based Access Control

It serves as a foundation for building scalable real estate management systems.
