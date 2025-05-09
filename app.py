from collections import deque

from flask import Flask, jsonify, render_template, request

from backend.main import make_request

previous_conversations: deque[str] = deque(maxlen=20)
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/gemini", methods=["POST"])
def gemini():
    user_input = request.form.get("text", "")

    if user_input == "":
        return jsonify({"error": "Empty text"})

    previous_conversations.append(user_input)
    user_request = list(previous_conversations)
    result = make_request(user_request)
    print(result)

    return jsonify({"result": result})


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "")
        email = request.form.get("email", "")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
