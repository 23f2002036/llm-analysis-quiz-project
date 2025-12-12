#!/usr/bin/env powershell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Push to HuggingFace Space" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To get your HuggingFace token:" -ForegroundColor Yellow
Write-Host "1. Go to https://huggingface.co/settings/tokens" 
Write-Host "2. Create a new token with 'write' access"
Write-Host "3. Copy the token and paste it below"
Write-Host ""

$HF_TOKEN = Read-Host "Enter your HuggingFace API token"

if ([string]::IsNullOrEmpty($HF_TOKEN)) {
    Write-Host "❌ No token provided. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Updating remote URL..." -ForegroundColor Cyan

# Update remote URL with token
git remote set-url hf "https://23F2002036:$HF_TOKEN@huggingface.co/spaces/23F2002036/tds-project-2.git"

Write-Host "Pushing to HuggingFace..." -ForegroundColor Cyan
git push hf main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to HuggingFace!" -ForegroundColor Green
    Write-Host "Space URL: https://huggingface.co/spaces/23F2002036/tds-project-2" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your Space will rebuild automatically. This may take a few minutes." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Failed to push. Check:" -ForegroundColor Red
    Write-Host "  - Your token is valid"
    Write-Host "  - Your token has 'write' access"
    Write-Host "  - You have internet connection"
}
