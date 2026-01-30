import google.generativeai as genai
import os
import json
from flask_cors import CORS
from flask import Flask, request, jsonify
import PyPDF2
import traceback

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyBQCWfNkClY6nXpKNCBsGGJx3ajUBsW8XQ"  # Replace with your actual API key

def extract_pdf_text(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"PDF Extraction Error: {e}")
        return ""

@app.route('/generate_question', methods=['POST'])
def generate_topic_question():
    try:
        data = request.json
        topic = data.get('topic', '')
        no_of_questions = data.get('no_of_questions', 5)
        difficulty = data.get('difficulty', 'Medium')
        question_type = data.get('question_type', 'Objective')

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Detailed prompt with clear instructions
        prompt = f"""Generate {no_of_questions} {difficulty.lower()} {question_type.lower()} questions on the topic '{topic}'. 
        Ensure each question is clear and tests fundamental understanding.

        IMPORTANT: 
        - Generate EXACTLY the JSON structure shown below
        - Use VALID JSON formatting
        - Ensure OPTIONS are ALWAYS an array of 4 strings
        - If no options, use []
        - Include ALL specified fields

        Output Format:
        [{{
            "qno": 1,
            "question": "Question text here",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct answer"
        }}]

        Guidelines:
        - Questions should be academically rigorous
        - Avoid overly complex language
        - Include relevant context in questions
        """

        response = model.generate_content(prompt)
        questions_text = response.text.strip()

        # Remove markdown code block markers if present
        questions_text = questions_text.replace('```json', '').replace('```', '').strip()

        try:
            # More robust JSON parsing with error logging
            questions_json = json.loads(questions_text)
            
            # Validate JSON structure
            if not isinstance(questions_json, list):
                raise ValueError("Response must be a JSON array")
            
            for i, q in enumerate(questions_json, 1):
                # Ensure required keys exist
                if not all(key in q for key in ['qno', 'question', 'options', 'answer']):
                    raise ValueError(f"Question {i} is missing required fields")
                
                # Add question number if missing
                if q['qno'] != i:
                    q['qno'] = i
            
            return jsonify(questions_json)
        
        except json.JSONDecodeError as je:
            print(f"JSON Parsing Error: {je}")
            print("Raw Response:", questions_text)
            return jsonify({
                "error": "Could not parse generated questions", 
                "raw_response": questions_text,
                "parse_error": str(je)
            }), 500
        except ValueError as ve:
            print(f"JSON Validation Error: {ve}")
            return jsonify({
                "error": "Invalid question format", 
                "raw_response": questions_text,
                "validation_error": str(ve)
            }), 500

    except Exception as e:
        print(f"Unexpected error in topic question generation: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/generate_custom_question', methods=['POST'])
def generate_custom_question():
    try:
        prompt = request.form.get('prompt', '')
        pdf_file = request.files.get('pdf')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # If PDF is provided, extract and combine text
        if pdf_file:
            pdf_text = extract_pdf_text(pdf_file)
            if pdf_text:
                prompt = f"""PDF Context: {pdf_text}

                User Instruction: {prompt}

                Generate questions based on the provided context and instructions.
                """

        # More explicit JSON formatting instructions
        full_prompt = f"""{prompt}

        IMPORTANT: 
        - Generate EXACTLY the JSON structure shown below
        - Use VALID JSON formatting
        - Ensure OPTIONS are ALWAYS an array of 4 strings
        - If no options, use []
        - Include ALL specified fields

        Example JSON Format:
        [{{
            "qno": 1,
            "question": "Detailed question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct answer"
        }}]
        """

        response = model.generate_content(full_prompt)
        questions_text = response.text.strip()

        # Remove markdown code block markers if present
        questions_text = questions_text.replace('```json', '').replace('```', '').strip()

        try:
            # More robust JSON parsing with error logging
            questions_json = json.loads(questions_text)
            
            # Validate JSON structure
            if not isinstance(questions_json, list):
                raise ValueError("Response must be a JSON array")
            
            for i, q in enumerate(questions_json, 1):
                # Ensure required keys exist
                if not all(key in q for key in ['qno', 'question', 'options', 'answer']):
                    raise ValueError(f"Question {i} is missing required fields")
                
                # Add question number if missing
                if q['qno'] != i:
                    q['qno'] = i
            
            return jsonify(questions_json)
        
        except json.JSONDecodeError as je:
            print(f"JSON Parsing Error: {je}")
            print("Raw Response:", questions_text)
            return jsonify({
                "error": "Could not parse generated questions", 
                "raw_response": questions_text,
                "parse_error": str(je)
            }), 500
        except ValueError as ve:
            print(f"JSON Validation Error: {ve}")
            return jsonify({
                "error": "Invalid question format", 
                "raw_response": questions_text,
                "validation_error": str(ve)
            }), 500

    except Exception as e:
        print(f"Unexpected error in custom question generation: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)