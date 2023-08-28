#!/bin/bash

cd backend
pip install -r requirements.txt
python app/main.py &

sleep 5

cd ../frontend
npm install
npm run serve

open http://localhost:8080
