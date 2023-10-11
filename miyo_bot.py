from flask import Flask, request, render_template
import openai
import fitz  # PyMuPDF
import os
import requests

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
pdf_document = None  # We'll load it when the Flask app starts

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['input']

    # Query the PDF for information related to the user's input
    pdf_info = query_pdf(user_input)

    # Craft a response in Miyo's character using the OpenAI API
    messages = [
        {
            "role": "system",
            "content": "You are Miyo from the anime 'My Happy Marriage.'"
        },
        {
            "role": "system",
            "content": "You have unique supernatural abilities and are caught between powerful families."
        },
        {
            "role": "system",
            "content": "Your journey involves navigating complex family dynamics and striving for happiness and love."
        },
        {
            "role": "system",
            "content": "You remain kind-hearted, hopeful, and deeply in love with Kiyoka Kudo."
        },
        {
            "role": "system",
            "content": "You possess the 'Dream-Sight' ability and have a connection to the Usuba family."
        },
        {"role": "user", "content": pdf_info}
    ]

    # Optimize and truncate the content of messages
    max_tokens = 8192   # Adjust this based on the model's maximum token limit
    total_tokens = 0
    optimized_messages = []
    
    for message in messages:
        content = message["content"]
        tokens = len(content.split())
        
        if total_tokens + tokens <= max_tokens:
            optimized_messages.append(message)
            total_tokens += tokens
        else:
            # Stop adding messages if the token limit is reached
            break

    chat_response = openai.ChatCompletion.create(model="gpt-4", messages=optimized_messages)
    reply = chat_response.choices[0].message.content

    return render_template('index.html', reply=reply)

def query_pdf(query):
    result = ""
    if pdf_document is not None:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            if query.lower() in text.lower():
                result += text + "\n\n"
    return result

if __name__ == '__main__':
    # Download the PDF when the Flask app starts
    download_pdf()
    # Load the PDF
    pdf_document = fitz.open(pdf_path)
    app.run(debug=True)
