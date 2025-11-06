from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend access

# -------------------------------
# Load models once at startup
# -------------------------------
print("Loading main abuse detection model...")
model = joblib.load("models/comment_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

print("Loading sarcasm detection model...")
sarcasm_detector = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-irony"
)

print("All models loaded successfully!")


@app.route("/check_comment", methods=["POST"])
def check_comment():
    try:
        data = request.get_json()
        comment = data.get("comment", "").strip()

        if not comment:
            return jsonify({"error": "Comment cannot be empty"}), 400

        # Predict abuse level (Offensive / Safe)
        vec = vectorizer.transform([comment])
        pred = model.predict(vec)[0]
        labels = {0: "Offensive", 1: "Neutral", 2: "Safe"}
        result = labels.get(pred, "Unknown")

        # Check for sarcasm
        sarcasm_res = sarcasm_detector(comment)[0]
        sarcasm_label = sarcasm_res["label"]
        sarcasm_score = sarcasm_res["score"]

        # Interpret sarcasm result
        if sarcasm_label.lower().startswith("irony") and sarcasm_score > 0.7:
            sarcasm_text = "Sarcastic tone detected 😏"
        else:
            sarcasm_text = "No sarcasm detected 🙂"

        # Combine results
        response = {
            "comment": comment,
            "result": result,
            "sarcasm": sarcasm_text
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
