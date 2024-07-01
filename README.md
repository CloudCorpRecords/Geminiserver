# Open-Source Gemini API Server for Frontend Code Generation

This repository provides an open-source backend server that uses Google's Gemini API to generate HTML, CSS, and JavaScript code from natural language descriptions. It's designed to power frontend code generation applications and tools.

## Features

- **Gemini Integration:**  Connects to Google's powerful Gemini large language model for code generation.
- **Prompt Engineering:**  Guides Gemini with specific instructions to generate well-structured frontend code.
- **Code Organization:**  Extracts and organizes the generated HTML, CSS, and JavaScript into a complete HTML document.
- **CORS Enabled:**  Allows cross-origin requests from your frontend application, making it easy to integrate.

## How it Works

1. **API Request:**  The frontend application sends a POST request to the `/generate` endpoint with a JSON payload containing the following:
    - **`prompt` (required):**  A natural language description of the frontend code to be generated.
    - **`model` (optional):**  The Gemini model to use (default: `gemini-1.5-flash`).
    - **`parameters` (optional):**  Additional parameters for the Gemini model (e.g., `temperature`, `max_output_tokens`).
2. **Prompt Enhancement:** The server adds context and instructions to the prompt to guide Gemini in generating well-structured code.
3. **Code Generation:** The Gemini API is called with the enhanced prompt.
4. **Code Extraction and Organization:**  The server extracts the generated CSS, JavaScript, and HTML code from Gemini's output and organizes them into a complete HTML document.
5. **Response:** The server sends back a JSON response with the generated HTML code.

## Setup

1. **Get a Gemini API Key:**
   - Visit [https://developers.generativeai.google.com/](https://developers.generativeai.google.com/) and create a project.
   - Enable the Gemini API and obtain an API key.

2. **Fork or Clone the Repository:**

   - Fork the repository to your own GitHub account or clone it:
     `git clone https://github.com/CloudCorpRecords/Geminiserver.git`

3. **Deploy on Replit:**

   - **Import the Repository:** Import your forked or cloned repository into a new Replit project.
   - **Add Your API Key:** Create a Replit Secret named `GEMINI_API_KEY` and store your Gemini API key as its value.
   - **Install Dependencies:** In the Replit Shell, run `pip install -r requirements.txt` to install the required packages.
   - **Deploy:** Click the "Deploy" button in Replit to fully deploy the server. You will get a URL for your API endpoint (e.g., `https://your-backend-server.repl.co/generate`).

## Usage

You can interact with this API server using any tool that can make HTTP requests (e.g., `curl`, `Postman`, or JavaScript's `fetch`). 

**Example Request using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"prompt": "Generate HTML and CSS for a webpage with a button that changes color on hover.", "model": "gemini-1.5-pro"}' \
     https://your-backend-server.repl.co/generate
Use code with caution.
Markdown
Replace https://your-backend-server.repl.co/generate with your actual API endpoint URL.
Open Source and OpenGenApps
This project is part of the OpenGenApps initiative by Rene Turcios, which aims to create open-source generative AI applications.
Contributing
Contributions are welcome! Please see the CONTRIBUTING.md file for guidelines.
License
This project is licensed under the MIT License.
**Key Points:**

- **Clear Explanation of Functionality:** The README provides a more detailed breakdown of how the server interacts with Gemini, processes prompts, and returns responses.
- **Deployment Instructions:**  Expanded instructions on setting up the server on Replit, including installing dependencies.
- **Emphasis on Open Source and OpenGenApps:** Highlights the project's open-source nature and its connection to the OpenGenApps initiative.
