from flask import Flask, jsonify, request
from model_utils import predict, load_model

app = Flask(__name__)

load_model()

@app.route("/")
def home():
    return jsonify({"message": "API is running"})

@app.route("/predict", methods=["POST"])
def predict_route():
    try:
        data = request.get_json()
        result = predict(data)
        return jsonify({"predicted_age": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
