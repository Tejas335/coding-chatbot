from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# store conversation
chat_history = []

# 🔴 your API key
API_KEY = "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"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    try:
        # 🔥 Debug mode detection
        if "fix this" in user_message.lower() or "debug" in user_message.lower():
            user_message = "Fix the following code and explain the errors clearly:\n\n" + user_message

        # add user message to history
        chat_history.append({
            "role": "user",
            "content": user_message
        })

        # API request
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a coding assistant.\n"
                            "If the user provides code, fix errors and explain clearly.\n"
                            "Always give corrected code and explanation separately.\n\n"
                            "Always write code clearly like this:\n\n"
                            "#include <stdio.h>\n"
                            "int main() {\n"
                            "    // code\n"
                            "}\n\n"
                            "Do not write code in one line. Keep it readable."
                        )
                    }
                ] + chat_history,
                "temperature": 0.7
            }
        )

        data = response.json()
        print("FULL RESPONSE:", data)

        # 🔥 Safe response handling
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = str(data)

        # add bot reply to history
        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Error occurred"})

if __name__ == "__main__":
    app.run(debug=True)