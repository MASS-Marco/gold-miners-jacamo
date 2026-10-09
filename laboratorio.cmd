@echo off
setlocal
cd /d "%~dp0"
if exist "%~dp0..\..\..\.venv-documentos\Scripts\python.exe" (
  "%~dp0..\..\..\.venv-documentos\Scripts\python.exe" -X utf8 scripts\laboratorio.py %*
) else (
  python -X utf8 scripts\laboratorio.py %*
)
exit /b %errorlevel%
