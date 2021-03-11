@echo off
FOR /F "tokens=*" %%g IN ('cd') do (SET cwd=%%g)
if exist %cwd%\virtualenv (
    goto RUN
    ) else (
    goto SETUP
)
:SETUP
FOR /F "tokens=*" %%g IN ('where python') do (SET python=%%g)
%python% -m venv virtualenv
%cwd%\virtualenv\Scripts\activate.bat && pip install -r %cwd%\requirements.txt && .\venv\Scripts\python.exe .\main.py

:RUN
.\venv\Scripts\python.exe .\main.py