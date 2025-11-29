# YouTube Trends Explorer - Full Stack Startup Script
# This script starts both the backend API and frontend UI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YouTube Trends Explorer - Full Stack" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Check if node_modules exists in frontend
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "❌ Frontend dependencies not installed!" -ForegroundColor Red
    Write-Host "Please run: cd frontend && npm install" -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 Starting Backend API..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\activate; Write-Host '🔧 Backend API Server' -ForegroundColor Cyan; Write-Host 'API: http://localhost:8000' -ForegroundColor Green; Write-Host 'Docs: http://localhost:8000/docs' -ForegroundColor Green; Write-Host ''; python run_api.py"

Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "🎨 Starting Frontend UI..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host '🎨 Frontend Development Server' -ForegroundColor Cyan; Write-Host 'UI: http://localhost:5173' -ForegroundColor Green; Write-Host ''; npm run dev"

Write-Host ""
Write-Host "✅ Full stack started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access Points:" -ForegroundColor Cyan
Write-Host "   Frontend UI:  http://localhost:5173" -ForegroundColor White
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: Close the PowerShell windows to stop the servers" -ForegroundColor Yellow
Write-Host ""
