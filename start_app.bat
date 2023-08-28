@echo off

cd backend
pip install -r requirements.txt
start /b python app\main.py

timeout /t 5 /nobreak

cd ..\frontend
npm install
npm run serve

start http://localhost:8080
