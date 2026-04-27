# Quick Setup Script for Neon.tech PostgreSQL
# This script helps you set up your .env file

Write-Host "🚀 DeepFake Detection - Neon.tech Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (Test-Path .env) {
    Write-Host "⚠️  .env file already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
    if ($overwrite -ne "y") {
        Write-Host "❌ Setup cancelled." -ForegroundColor Red
        exit
    }
}

Write-Host ""
Write-Host "📝 Please provide your Neon.tech connection details:" -ForegroundColor Green
Write-Host ""
Write-Host "Get your connection string from: https://console.neon.tech/" -ForegroundColor Gray
Write-Host "Example: postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require" -ForegroundColor Gray
Write-Host ""

$databaseUrl = Read-Host "Enter your DATABASE_URL"

# Generate a random secret key
$secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})

Write-Host ""
Write-Host "🔑 Admin Credentials Setup:" -ForegroundColor Green
$adminEmail = Read-Host "Admin Email (default: admin@deepfake.com)"
if ([string]::IsNullOrWhiteSpace($adminEmail)) {
    $adminEmail = "admin@deepfake.com"
}

$adminPassword = Read-Host "Admin Password (default: admin123)"
if ([string]::IsNullOrWhiteSpace($adminPassword)) {
    $adminPassword = "admin123"
}

# Create .env file
$envContent = @"
# Database - Neon.tech PostgreSQL
DATABASE_URL=$databaseUrl

# JWT Settings
SECRET_KEY=$secretKey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin Credentials
ADMIN_EMAIL=$adminEmail
ADMIN_PASSWORD=$adminPassword

# File Upload Settings
UPLOAD_DIR=uploads
MAX_FILE_SIZE=104857600
"@

$envContent | Out-File -FilePath .env -Encoding UTF8

Write-Host ""
Write-Host "✅ .env file created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Make sure PostgreSQL driver is installed: pip install -r requirements.txt" -ForegroundColor White
Write-Host "2. Initialize database: python -m app.init_db" -ForegroundColor White
Write-Host "3. Run the server: uvicorn main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Visit http://localhost:8000/docs to test your API!" -ForegroundColor Green
Write-Host ""
