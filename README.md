📄 Automated Question Paper Generator using Generative AI
🧠 Overview

The Automated Question Paper Generator is an AI-powered system designed to simplify and automate the creation of examination question papers for educational institutions. It reduces faculty workload by generating exam-ready question papers based on topics or syllabus PDFs, while strictly following institutional formatting standards.

✨ Key Features

📝 Create by Topic
Generate objective (MCQs) or subjective questions by providing:

Topic name

Number of questions
Difficulty level (Easy / Medium / Hard)
Question type

📂 Create by Choice (PDF-Based)
Upload a syllabus or reference PDF and provide a short prompt to generate syllabus-aligned questions.

🎯 Difficulty Control
Ensures balanced and relevant question difficulty.

🔁 Non-Repetitive Questions
Prompt engineering and validation prevent duplication.

🏫 College-Specific Format
Automatically formats papers according to the VIT Pune question paper template.

📥 Downloadable PDF
Generates a complete, exam-ready question paper.

🛠️ Technology Stack

🐍 Backend: Flask (Python)
🤖 AI Model: Google Gemini 1.5 Flash API
📬 API Testing: Postman
📄 PDF Processing: PyPDF2
🔍 OCR: Optical Character Recognition (for scanned PDFs)
🌐 Frontend: HTML, CSS, JavaScript
🔗 Architecture: RESTful APIs (Stateless)

🔄 System Workflow

User selects Create by Topic or Create by Choice
Inputs are sent to the Flask backend via REST APIs
PDF text is extracted using PyPDF2 or OCR
A structured prompt is generated
Prompt is sent to the Gemini AI API
AI generates relevant, non-repeating questions
Questions are formatted into the VIT template
Final question paper is generated as a downloadable PDF

⚡ Why Gemini 1.5 Flash?

🚀 Fast response time
📚 Handles large syllabus content
💰 Cost-efficient for production use
🧩 No model training required
🔄 Ideal for real-time academic applications

🗄️ Database Usage

This system does not use a database. It is designed to be stateless, allowing easy integration into existing institutional platforms without persistent storage dependency.

🧪 API Testing

All backend APIs were tested using Postman to ensure:
Correct request handling
Proper AI integration
Error management
Performance optimization
