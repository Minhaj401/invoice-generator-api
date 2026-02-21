@echo off
REM GitHub Setup Script for Invoice Generator API

echo.
echo ===================================
echo GitHub Repository Setup
echo ===================================
echo.

REM Add GitHub CLI to PATH for this session
set "PATH=%PATH%;C:\Program Files\GitHub CLI"

echo Step 1: Authenticating with GitHub...
echo Please follow the browser prompts to authenticate.
echo.

REM Authenticate with GitHub - choose HTTPS and default settings
echo HTTPS | gh auth login --web --hostname github.com

echo.
echo Step 2: Creating GitHub repository...
gh repo create invoice-generator-api --public --description "Flask API for generating PDF invoices from chat messages with AI parsing and UPI QR code integration" --source=. --remote=origin --push

echo.
echo ===================================
echo Setup Complete!
echo ===================================
echo Your repository is now on GitHub!
echo.
echo Next steps:
echo 1. Visit: https://github.com/%USERNAME%/invoice-generator-api
echo 2. Deploy to Railway from the repository
echo.
pause
