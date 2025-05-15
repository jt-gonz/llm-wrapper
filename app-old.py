from collections import deque

from flask import Flask, jsonify, render_template, request

from backend.main import make_request, validate_credentials
from frontend import create_app

previous_conversations: deque[str] = deque(maxlen=20)
app = create_app()


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


@app.route("/login", methods=["POST"])
def login():
    user_email = request.form.get("email", "")
    user_password = request.form.get("password", "")

    if not user_email or not user_password:
        return jsonify({"error": "Error processing email or password."}), 400

    result = validate_credentials(user_email, user_password)
    if result is True:
        return jsonify({"status": "Login successful"}), 200
    else:
        return jsonify({"status": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
