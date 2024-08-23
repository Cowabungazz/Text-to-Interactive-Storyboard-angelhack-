# Project Overview
Our team aims to address the financial literacy gap among the elderly population in Singapore by transforming complex financial content into engaging and personalised scenario-based learning. The solution leverages a combination of Gen-AI to easily simulate scenarios in the form of interactive storyboards to make financial education more accessible, comprehensible and impactful for the elderly. 

# .env to be included 
- OPENAI_API_KEY='sk-proj....ceP5Q'
- MONGO_DETAILS=mongodb+srv://changzenn:...@cluster0.h9mxlnf.mongodb.net/mydatabase?retryWrites=true&w=majority
- api_key = 'AIza...6cYH0'
- EMAIL_VALIDATION_KEY = '290f98e...303c'

# How to start backend
## 1) Install Requirements
- cd Backend
- pip install -r requirements

## 2) Run Backend
- uvicorn main:app --reload

# How to start frontend 
## 1) Install Requirements 
- cd frontend
- npm install

## 2) Run Frontend
- npm run dev
