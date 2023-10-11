from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = "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"
pdf_url = "https://drive.google.com/uc?export=download&id=1Oe2UuK0Yps4eRyCIUvEsugQuN4jxGKjz"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['input']
    
    # For now, we'll just return the user's input. Integration with chatwithpdf will come in later steps.
    return jsonify({"reply": user_input})

if __name__ == '__main__':
    app.run(port=5000)
