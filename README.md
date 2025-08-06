I recently worked on a project that transforms dense financial articles into interactive storyboards tailored for elderly learners. We built a FastAPI backend with two key endpoints: one that accepts raw text and another that accepts a link to an article. Both routes funnel the content into an asynchronous GPT service, which prompts a model like GPT‑3.5 to return a fully structured JSON lesson. Each lesson is composed of scenes, and every scene has dialogue, an array of icon objects—each positioned by x and y coordinates—and a “branching” node that describes decision points and the next scene IDs. We validate the JSON against a Pydantic data model to catch malformed responses early, then store the lesson and any associated icon metadata in MongoDB via Motor’s async client. On the front end we used a simple React/Vite setup to render the scenes sequentially, parsing the branching logic so that a learner can choose different paths and see the consequences, all while displaying icons such as a piggy bank, a calculator, or a “next” arrow to keep navigation intuitive. For example, when a user uploads an article on retirement savings, the system might generate an opening scene where “Mr. Tan” meets a financial advisor; the learner chooses between “deposit into CPF” or “open a low‑risk investment,” and each choice leads to a new scene with different icons and narrative outcomes. I was mainly responsible for designing the lesson schema, writing the GPT prompt logic, and ensuring the entire pipeline remained nonblocking by leveraging async/await throughout the controllers and MongoDB operations.

# Demo
https://www.youtube.com/watch?v=BQCdGOXC05s&t=2s
<img width="1374" height="717" alt="image" src="https://github.com/user-attachments/assets/ac1aa881-6ad6-44df-843b-431f3a3ec808" />
<img width="1375" height="715" alt="image" src="https://github.com/user-attachments/assets/281a5711-7a5e-477d-b94d-25b1e5be8f60" />
<img width="1373" height="717" alt="image" src="https://github.com/user-attachments/assets/18f96fc8-8643-4bcc-bbc1-dce91291196b" />

# Project Overview
Addressing the financial literacy gap among the elderly population in Singapore by transforming complex financial content into engaging and personalised scenario-based learning. The solution leverages a combination of Gen-AI to easily simulate scenarios in the form of interactive storyboards to make financial education more accessible, comprehensible and impactful for the elderly. 

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
