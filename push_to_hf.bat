@echo off
REM Script to push to HuggingFace with token

echo ========================================
echo Push to HuggingFace Space
echo ========================================
echo.
echo To get your HuggingFace token:
echo 1. Go to https://huggingface.co/settings/tokens
echo 2. Create a new token with 'write' access
echo 3. Copy the token
echo.

set /p HF_TOKEN=Enter your HuggingFace API token: 

REM Update remote URL with token
git remote set-url hf https://23F2002036:%HF_TOKEN%@huggingface.co/spaces/23F2002036/llm-analysis-quiz-proj.git

echo.
echo Pushing to HuggingFace...
git push hf main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Successfully pushed to HuggingFace!
    echo Space URL: https://huggingface.co/spaces/23F2002036/llm-analysis-quiz-proj
) else (
    echo.
    echo ❌ Failed to push. Check your token and try again.
)

pause
