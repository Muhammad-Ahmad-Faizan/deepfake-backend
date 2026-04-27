# DeepFake Detection API - Backend

FastAPI backend for video and audio deepfake detection system.

## 🚀 Features

- **User Authentication**: JWT-based authentication with role-based access (User/Admin)
- **Video/Audio Upload**: Support for multiple video and audio formats
- **Deepfake Detection**: AI-powered analysis (dummy implementation included)
- **User Dashboard**: Track uploads, analysis results, and statistics
- **Admin Panel**: User management and system-wide statistics

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Setup Instructions

### 1. Create Virtual Environment

```powershell
# Navigate to backend directory
cd deep-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install Dependencies

```powershell
# Make sure venv is activated (you should see (venv) in your terminal)
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```powershell
# Copy the example env file
copy .env.example .env

# Edit .env file and update:
# - DATABASE_URL (your Neon.tech PostgreSQL connection string)
# - SECRET_KEY (use a strong random key for production)
# - ADMIN_EMAIL and ADMIN_PASSWORD (default admin credentials)
```

**🗄️ Using Neon.tech PostgreSQL (Recommended):**

See [NEON_SETUP.md](NEON_SETUP.md) for detailed instructions on setting up a free PostgreSQL database on Neon.tech.

Quick steps:

1. Create account at https://neon.tech/
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in `.env`

**Or use local SQLite:**

```env
DATABASE_URL=sqlite:///./deepfake_detection.db
```

### 4. Initialize Database

```powershell
# Run the database initialization script
python -m app.init_db
```

This will:

- Create the SQLite database
- Set up all tables
- Create a default admin user

### 5. Run the Server

```powershell
# Start the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication

- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user

### Upload

- `POST /api/upload/video` - Upload video/audio file
- `GET /api/upload/videos` - Get all user's videos
- `GET /api/upload/videos/{video_id}` - Get specific video
- `DELETE /api/upload/videos/{video_id}` - Delete video

### Predictions

- `POST /api/predictions/{video_id}/analyze` - Start analysis
- `GET /api/predictions/{video_id}/result` - Get prediction result
- `GET /api/predictions/{video_id}/status` - Check analysis status

### Dashboard

- `GET /api/dashboard/stats` - Get user statistics
- `GET /api/dashboard/recent-activity` - Get recent uploads

### Admin (Requires Admin Role)

- `GET /api/admin/stats` - Get system statistics
- `GET /api/admin/users` - Get all users
- `GET /api/admin/users/{user_id}` - Get user details
- `PATCH /api/admin/users/{user_id}` - Update user
- `DELETE /api/admin/users/{user_id}` - Delete user
- `GET /api/admin/videos` - Get all videos

## 🔑 Default Admin Credentials

```
Email: admin@deepfake.com
Password: admin123
```

**⚠️ IMPORTANT**: Change these credentials in production!

## 📖 How FastAPI Works

### Key Concepts:

1. **Routes/Endpoints**: Define using decorators like `@router.post("/endpoint")`
2. **Type Hints**: Python type hints enable automatic validation
3. **Pydantic Models**: Define request/response schemas
4. **Dependency Injection**: Use `Depends()` for authentication, database sessions
5. **Auto Documentation**: Swagger UI auto-generated from your code

### Example Request Flow:

```python
# 1. Client sends request
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

# 2. FastAPI validates request using Pydantic schema
# 3. Route handler processes the request
# 4. Returns validated response
{
  "access_token": "eyJ0eXAiOiJKV1...",
  "token_type": "bearer",
  "user": {...}
}
```

## 🔒 Authentication Flow

1. User signs up or logs in
2. Server generates JWT token
3. Client stores token
4. Client sends token in Authorization header: `Bearer <token>`
5. Server validates token for protected routes

## 📁 Project Structure

```
deep-backend/
├── app/
│   ├── __init__.py
│   ├── auth.py           # JWT & password handling
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── utils.py          # Utility functions
│   ├── init_db.py        # Database initialization
│   └── routes/
│       ├── __init__.py
│       ├── auth.py       # Authentication routes
│       ├── upload.py     # Upload routes
│       ├── predictions.py # Prediction routes
│       ├── dashboard.py  # Dashboard routes
│       └── admin.py      # Admin routes
├── uploads/              # Uploaded files (auto-created)
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md           # This file
```

## 🧪 Testing the API

### Using the Interactive Docs (Recommended)

1. Go to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

### Using curl or Postman

```powershell
# Sign up a new user
curl -X POST "http://localhost:8000/api/auth/signup" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'

# Login
curl -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Upload video (replace TOKEN with your JWT token)
curl -X POST "http://localhost:8000/api/upload/video" `
  -H "Authorization: Bearer TOKEN" `
  -F "file=@path/to/video.mp4"
```

## 🔄 Next Steps

1. **Integrate Real AI Model**: Replace dummy prediction in `app/routes/predictions.py`
2. **Add File Storage**: Use cloud storage (AWS S3, Azure Blob) instead of local files
3. **Add Email Verification**: Implement email confirmation for new users
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Logging**: Implement proper logging system
6. **Tests**: Write unit and integration tests
7. **Docker**: Create Dockerfile for easy deployment

## 🐛 Troubleshooting

### venv activation issues

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module not found errors

Make sure venv is activated and dependencies are installed:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Database errors

Delete the database file and reinitialize:

```powershell
Remove-Item deepfake_detection.db
python -m app.init_db
```

## 📞 Support

For issues or questions about FastAPI:

- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

---

**Happy Coding! 🚀**
