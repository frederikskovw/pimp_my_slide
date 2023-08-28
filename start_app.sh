#!/bin/bash

# Navigate to backend and set it up
cd backend
pip install -r requirements.txt
python app/main.py &

# Wait for a few seconds to ensure backend starts up
sleep 5

# Navigate to frontend and set it up
cd ../frontend
npm install
npm run serve

# Open the application in a web browser (optional)
open http://localhost:8080
