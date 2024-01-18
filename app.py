import json
import re
import Levenshtein
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open("data-[SANITIZED].json", "r", encoding="utf-8") as file:
    chat_data = json.load(file)

def calculate_similarity(query, message):
    return Levenshtein.ratio(query.lower(), message.lower())

def get_bot_response(query):
    matching_responses = []
    best_similarity = 0.0

    for idx, message in enumerate(chat_data):
        similarity = calculate_similarity(query, message["message"])
        if similarity > 0.7 and idx < len(chat_data) - 1:
            next_message = chat_data[idx + 1]
            if message["sender"] == next_message["receiver"]:
                matching_responses.append(next_message["message"])
                best_similarity = similarity

    if matching_responses:
        bot_response = random.choice(matching_responses)
    else:
        bot_response = "Bot couldn't find a matching response."

    return (bot_response, best_similarity)

@app.route('/', methods=['GET']) # type: ignore
def index():
    if request.method == 'GET':
            # return render_template("index.html")
            return 'Welcome to the chatbot! Use POST method to send queries.'
    
@app.route('/prompt', methods=['POST','GET'])
def chat():
    if request.method == 'GET':
        if "prompt" in request.args and not request.args.get("prompt") == "":
            prompt = request.args.get("prompt")
        else:
            return jsonify({"error": "prompt parameter is missing."}), 400
    else:
        if "prompt" in request.form and not request.form["prompt"] == "":
            prompt = request.form["prompt"]
        else:
            return jsonify({"error": "prompt is missing."}), 400

    response, similarity = get_bot_response(prompt)
    return jsonify({
        'query': prompt,
        'response': response.strip(),
        'similarity': similarity,
    })

if __name__ == "__main__":
    app.run(debug=False, port=20060)
