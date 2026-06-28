from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "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"   # ⚠️ use NEW key (delete old one)

@app.route("/review", methods=["POST"])
def review():
    try:
        data = request.json
        code = data.get("code")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",   # ✅ FIXED LINE
                "messages": [
                    {"role": "user", "content": f"Review this code:\n{code}"}
                ]
            }
        )

        result = response.json()

        # DEBUG
        print("FULL RESPONSE:", result)

        if "choices" in result:
            return jsonify({
                "review": result["choices"][0]["message"]["content"]
            })
        else:
            return jsonify({
                "review": "API Error: " + str(result)
            })

    except Exception as e:
        return jsonify({
            "review": "Server Error: " + str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)