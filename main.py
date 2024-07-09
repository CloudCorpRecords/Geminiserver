import html
import os
import re
import traceback

import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the API key from the Replit secret
my_secret = os.environ['GEMINI_API_KEY']
genai.configure(api_key=my_secret)


def extract_content(text, tag):
    pattern = f"<{tag}>(.*?)</{tag}>"
    content = re.findall(pattern, text, re.DOTALL)
    return content[0].strip() if content else ""


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

        
        # Remove markdown tags from response text
        response_text = re.sub(r'```html', '', response.text)
        response_text = re.sub(r'```', '', response_text)

        print("Raw response:", response.text)  # Log the raw response
        
        # Extract CSS, JavaScript, and HTML
        css = re.findall(r"<style>(.*?)</style>", response_text, re.DOTALL)
        css = css[0] if css else ""
        javascript = re.findall(r"<script>(.*?)</script>", response_text,
                                re.DOTALL)
        javascript = javascript[0] if javascript else ""
        html_content = re.sub(r"<style>.*?</style>",
                              "",
                              response_text,
                              flags=re.DOTALL)
        html_content = re.sub(r"<script>.*?</script>",
                              "",
                              html_content,
                              flags=re.DOTALL)
        html_content = html_content.strip()

        print("Extracted CSS:", css)  # Log the extracted CSS
        print("Extracted JavaScript:", javascript)  # Log the extracted JavaScript
        print("Extracted HTML:", html_content)  # Log the extracted HTML

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

        response_data = {
            'complete_html': escaped_html,
            'html': html_content,
            'css': css,
            'js': javascript
        }

        print("Response data:", response_data)  # Log the response data

        return jsonify(response_data)

    except Exception as e:
        print("Error occurred:", str(e))
        print("Traceback:", traceback.format_exc())
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
