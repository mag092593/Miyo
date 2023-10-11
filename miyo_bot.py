from flask import Flask, request, render_template
import openai
import fitz  # PyMuPDF
import os
import requests
import random

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

# PDF URL
pdf_url = "https://drive.google.com/uc?export=download&id=1Oe2UuK0Yps4eRyCIUvEsugQuN4jxGKjz"

# Define the local file path where you want to save the PDF
pdf_path = "my_pdf.pdf"

# Download the PDF from the URL and save it locally
def download_pdf():
    response = requests.get(pdf_url)
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(response.content)

# Load the PDF when the server starts
pdf_document = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['input']
    reply = "I'm sorry, I couldn't understand that."  # Default reply

    # Query the PDF for information related to the user's input
    pdf_info = query_pdf(user_input)

    # If the PDF query returns None, craft a response using Miyo's character
    if pdf_info is None or pdf_info == "":
        pdf_info = random.choice([
            "You are Miyo from the anime 'My Happy Marriage.'",
            "You have unique supernatural abilities and are caught between powerful families.",
            "Your journey involves navigating complex family dynamics and striving for happiness and love.",
            "You remain kind-hearted, hopeful, and deeply in love with Kiyoka Kudo.",
            "You possess the 'Dream-Sight' ability and have a connection to the Usuba family."
        ])

    messages = [
        {"role": "system", "content": "You are Miyo from the anime 'My Happy Marriage.'"},
        {"role": "system", "content": "You have unique supernatural abilities and are caught between powerful families."},
        {"role": "system", "content": "Your journey involves navigating complex family dynamics and striving for happiness and love."},
        {"role": "system", "content": "You remain kind-hearted, hopeful, and deeply in love with Kiyoka Kudo."},
        {"role": "system", "content": "You possess the 'Dream-Sight' ability and have a connection to the Usuba family."},
        {"role": "user", "content": pdf_info}
    ]

    prompt = "\n".join([msg["content"] for msg in messages])

    try:
        chat_response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150)
        if chat_response.choices and chat_response.choices[0].text:
            reply = chat_response.choices[0].text.strip()
    except Exception as e:
        reply = f"Error: {str(e)}"

    return render_template('index.html', reply=reply)

def query_pdf(query):
    result = ""
    if pdf_document is not None:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            if query.lower() in text.lower():
                result += text + "\n\n"
        if not result:
            return None
    return result

if __name__ == '__main__':
    # Download the PDF when the Flask app starts
    download_pdf()
    # Load the PDF
    pdf_document = fitz.open(pdf_path)
    app.run(debug=True)
