from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
import html
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the API key from the Replit secret
my_secret = os.environ['GEMINI_API_KEY']  
genai.configure(api_key=my_secret)

@app.route('/generate', methods=['POST'])
def generate_text():
    """
    Generates frontend code using the Gemini API, placing CSS and JS in the correct locations.

    Request Body (JSON):
    {
        "prompt": "Description of the desired frontend code (required)",
        "model": "Gemini model (optional, default: 'gemini-1.5-flash')",
        "parameters": { ... } 
    }

    Response (JSON):
    {
        "text": "The generated HTML code" 
    }

    Errors:
    - 400 Bad Request if the 'prompt' is missing.
    - 500 Internal Server Error for other issues.
    """

    try:
        data = request.get_json()
        prompt = data.get('prompt')
        model_name = data.get('model', 'gemini-1.5-flash')
        parameters = data.get('parameters', {})

        if not prompt:
            return jsonify({'error': 'Missing "prompt" in request body'}), 400

        # Enhanced prompt with instructions
        prompt =  "You are an expert frontend developer. " \
                  "Generate only the HTML, CSS, and JavaScript code, without explanations. " \
                  "Place all CSS within a <style> tag in the <head> of the HTML. " \
                  "Place all JavaScript within a <script> tag at the end of the <body>. " \
                  f"{prompt}" 

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt, **parameters)

        # Extract CSS, JavaScript, and HTML
        css = re.findall(r"<style>(.*?)</style>", response.text, re.DOTALL)
        css = css[0] if css else ""
        javascript = re.findall(r"<script>(.*?)</script>", response.text, re.DOTALL)
        javascript = javascript[0] if javascript else ""
        html_content = re.sub(r"<style>.*?</style>", "", response.text, flags=re.DOTALL)
        html_content = re.sub(r"<script>.*?</script>", "", html_content, flags=re.DOTALL)

        # Construct the complete HTML structure
        complete_html = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
  {css}
  </style>
</head>
<body>
  {html_content}
  <script>
  {javascript}
  </script>
</body>
</html>
        """

        # Escape HTML tags for safe display 
        escaped_html = html.escape(complete_html)

        return jsonify({'text': escaped_html})  # Send back the complete HTML

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)