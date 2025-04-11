from flask import Flask, jsonify, render_template, request

from backend.main import make_request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/gemini", methods=["POST"])
def gemini():
    user_input = request.form.get("text", "")

    if user_input == "":
        return jsonify({"error": "Empty text"})

    result = make_request(user_input)
    print(result)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
