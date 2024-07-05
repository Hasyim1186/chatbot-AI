from flask import Flask, request, jsonify, render_template, url_for
from config import generation_config, system_instruction, api_key
from model import model, genai
from sentiment import analyze_sentiment

app = Flask(__name__)

negative_sentiment_count = {}
keywords = []

# Load keywords from file
def load_keywords():
    global keywords
    with open('keywords.txt', 'r', encoding='utf-8') as file:
        keywords = [line.strip() for line in file.readlines()]

load_keywords()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id', '')
    message = data.get('message', '')

    # Check for specific keywords related to self-harm or suicide
    if any(keyword in message.lower() for keyword in keywords):
        return jsonify({"redirect": url_for('psikolog')})

    # Initialize user's negative sentiment count if not present
    if user_id not in negative_sentiment_count:
        negative_sentiment_count[user_id] = 0

    history = [{"role": "user", "parts": [message]}]
    response = model.start_chat(history=history).send_message(message)
    model_response = response.text

    # Sentiment analysis
    sentiment_result = analyze_sentiment(message)

    if sentiment_result == 'negative':
        negative_sentiment_count[user_id] += 1

    if negative_sentiment_count[user_id] >= 10:
        return jsonify({"response": model_response, "sentiment": sentiment_result, "prompt_psikolog": "Apakah Anda ingin berkonsultasi dengan psikolog?", "redirect": url_for('psikolog')})

    return jsonify({"response": model_response, "sentiment": sentiment_result})

@app.route('/psikolog')
def psikolog():
    return render_template('psikolog.html')

if __name__ == '__main__':
    app.run(debug=True)
