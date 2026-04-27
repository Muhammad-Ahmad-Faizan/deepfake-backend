# 🚀 Setting Up Neon.tech PostgreSQL Database

This guide will help you set up a free PostgreSQL database on Neon.tech for your DeepFake Detection API.

## 📝 Step 1: Create Neon.tech Account

1. Go to https://neon.tech/
2. Click **"Sign Up"** (you can use GitHub, Google, or email)
3. Verify your email if required

## 🗄️ Step 2: Create a New Database

1. After logging in, click **"Create a project"**
2. Configure your project:
   - **Project name**: `deepfake-detection` (or any name you like)
   - **Database name**: `neondb` (default is fine)
   - **Region**: Choose closest to you (e.g., US East, EU West)
   - **PostgreSQL version**: Latest stable version
3. Click **"Create project"**

## 🔑 Step 3: Get Your Connection String

1. After project creation, you'll see a connection string
2. It looks like this:
   ```
   postgresql://username:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
3. **Important**: Copy this connection string - you'll need it!

### Finding it again:

- Go to your project dashboard
- Click on **"Connection Details"** or **"Dashboard"**
- You'll see the connection string under **"Connection string"**

## ⚙️ Step 4: Update Your Backend Configuration

1. **Open your `.env` file** (in `deep-backend` folder)
2. **Update the DATABASE_URL**:

   ```env
   DATABASE_URL=postgresql://your-username:your-password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```

   Replace with your actual connection string from Neon.tech

3. **Keep other settings**:

   ```env
   # JWT Settings
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Admin Credentials
   ADMIN_EMAIL=admin@deepfake.com
   ADMIN_PASSWORD=admin123

   # File Upload Settings
   UPLOAD_DIR=uploads
   MAX_FILE_SIZE=104857600
   ```

## 📦 Step 5: Install PostgreSQL Driver

Make sure your virtual environment is activated:

```powershell
# Navigate to backend folder
cd E:\Downloads\deep-fake\deep-backend

# Activate venv
.\venv\Scripts\Activate.ps1

# Install/update dependencies (includes psycopg2-binary)
pip install -r requirements.txt
```

## 🔨 Step 6: Initialize Database

Run the database initialization script to create tables and admin user:

```powershell
# Make sure you're in deep-backend folder and venv is activated
python -m app.init_db
```

You should see:

```
🔧 Initializing database...
✅ Admin user created: admin@deepfake.com
✅ Database initialized successfully!
```

## 🚀 Step 7: Run Your Application

```powershell
uvicorn main:app --reload
```

Visit http://localhost:8000/docs to test the API!

## ✅ Verify Connection

### Using Neon.tech Dashboard:

1. Go to your Neon.tech project
2. Click on **"Tables"** in the sidebar
3. You should see your tables: `users`, `videos`

### Using API:

1. Go to http://localhost:8000/docs
2. Try the login endpoint with admin credentials:
   - Email: `admin@deepfake.com`
   - Password: `admin123`
3. If it works, your database is connected! 🎉

## 💡 Neon.tech Free Tier Limits

- ✅ **3 projects** (databases)
- ✅ **0.5 GB storage** per project
- ✅ **Unlimited compute hours** (serverless)
- ✅ **Auto-suspend after 5 min of inactivity** (saves resources)

Perfect for development and small projects!

## 🔧 Troubleshooting

### Error: "could not connect to server"

- ✅ Check your internet connection
- ✅ Verify the connection string is correct
- ✅ Make sure `?sslmode=require` is at the end

### Error: "password authentication failed"

- ✅ Copy the connection string again from Neon.tech
- ✅ Password might contain special characters - use the full string as-is

### Error: "psycopg2 not installed"

```powershell
pip install psycopg2-binary
```

### Want to reset the database?

In Neon.tech dashboard:

1. Go to **"Settings"**
2. Click **"Delete project"** (creates a new one)

Or drop tables via SQL:

1. Go to **"SQL Editor"** in Neon.tech
2. Run:
   ```sql
   DROP TABLE IF EXISTS videos CASCADE;
   DROP TABLE IF EXISTS users CASCADE;
   ```
3. Run `python -m app.init_db` again

## 📊 Viewing Your Data

### Neon.tech SQL Editor:

1. Click **"SQL Editor"** in sidebar
2. Run queries:

   ```sql
   -- View all users
   SELECT * FROM users;

   -- View all videos
   SELECT * FROM videos;

   -- Count records
   SELECT COUNT(*) FROM users;
   ```

## 🔄 Switching Between SQLite (Local) and PostgreSQL (Neon)

Just change the `DATABASE_URL` in your `.env` file:

**For Neon.tech (PostgreSQL):**

```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

**For local SQLite:**

```env
DATABASE_URL=sqlite:///./deepfake_detection.db
```

Then restart your server!

## 🔐 Security Tips

1. **Never commit `.env` file** to Git (it's in `.gitignore`)
2. **Change admin password** after first login
3. **Use strong SECRET_KEY** in production
4. **Rotate database password** periodically in Neon.tech settings

## 📚 Additional Resources

- Neon.tech Docs: https://neon.tech/docs
- Connection Pooling: https://neon.tech/docs/connect/connection-pooling
- SQLAlchemy + PostgreSQL: https://docs.sqlalchemy.org/

---

**You're all set! Your backend is now using Neon.tech PostgreSQL! 🎉**
