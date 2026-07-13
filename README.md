# 🏡 Real Estate Property Listing Application

A full-stack **Real Estate Property Listing Application** built using **FastAPI, React, PostgreSQL, Docker, and JWT Authentication**.

The application allows users to browse, search, and manage real estate properties. It provides secure authentication, role-based access control, property management, favorites, reviews, amenities, notifications, and a responsive React frontend.

---

# 📌 Table of Contents

- Features
- Tech Stack
- Project Structure
- Project Setup
- Backend Setup
- Frontend Setup
- API Documentation
- API Modules
- Database
- Useful Commands
- Future Improvements
- Author

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
- 🏠 Seller
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

## Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy Async
- AsyncPG
- Pydantic
- Uvicorn
- Alembic
- JWT Authentication

## Frontend

- React
- Vite
- Axios
- CSS

## Database

- PostgreSQL

## Tools

- Docker
- Docker Compose
- pgAdmin
- Postman
- Git
- GitHub
- VS Code

---

# 📂 Project Structure

```text
Real-Estate-Property-Listing-App/
│
├── app/
├── frontend/
├── docker/
├── alembic/
├── tests/
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

---

# 🚀 Project Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/bhavanibapani-30/Real-Estate-property-listing-app.git
```

Move into the project folder.

```bash
cd Real-Estate-property-listing-app
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Create Environment File

Create a `.env` file inside the project root.

Example:

```env
DATABASE_URL=
JWT_SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=
```

⚠️ Never commit your `.env` file to GitHub.

---

# 🐳 PostgreSQL Docker Setup

Navigate to the docker folder.

```bash
cd docker
```

Start Docker containers.

```bash
docker compose start
```

Verify running containers.

```bash
docker ps
```

---

# ▶️ Run Backend

Return to the project root.

```bash
cd ..
```

Run the backend.

```bash
python run.py
```

Backend runs at:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

# 💻 Run Frontend

Open a new terminal.

Navigate to the frontend folder.

```bash
cd frontend
```

Install dependencies (first time only).

```bash
npm install
```

Run React.

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:3000
```

---

# ▶️ Project Startup Order

### Step 1

Start PostgreSQL.

```bash
cd docker
docker compose start
docker ps
```

---

### Step 2

Run Backend.

```bash
cd ..
python run.py
```

---

### Step 3

Open a new terminal.

---

### Step 4

Run Frontend.

```bash
cd frontend
npm install
npm run dev
```

---

# 📖 API Documentation

### Swagger UI

```
http://localhost:8000/docs
```

### ReDoc

```
http://localhost:8000/redoc
```

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

# 👩‍💻 Author

**Bhavani Bapani**

GitHub:

https://github.com/bhavanibapani-30

---

# 📄 License

This project is developed for learning and educational purposes.

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