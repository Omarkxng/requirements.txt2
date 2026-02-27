import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)
@app.route('/trading-webhook', methods=['GET', 'POST'])
# 2026 SDK Setup
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def home():
    return "Bot is Online", 200

@app.route('/trading-webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return "No JSON received", 400

    # Ask Gemini for a verdict
    prompt = f"Analyze {data.get('ticker')} {data.get('action')} at {data.get('price')}. Verdict: [YES/NO] + 5 words."
    response = client.models.generate_content(
        model="gemini-3.1-flash", 
        contents=prompt
    )

    print(f"Signal: {data.get('ticker')} | AI: {response.text}")
    return jsonify({"status": "ok", "verdict": response.text}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
