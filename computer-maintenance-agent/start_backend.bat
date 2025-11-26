@echo off
REM Start backend reading backend\.env if present
if exist backend\.env (
  for /f "usebackq tokens=1,* delims==" %%A in ("backend\.env") do (
    set "%%A=%%B"
  )
) else (
  echo backend\.env not found. Copy backend\.env.example to backend\.env and edit.
)

REM Use venv python
set PY="%~dp0.venv\Scripts\python.exe"
%PY% backend\app.py
