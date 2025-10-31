from flask import Flask, render_template, request, jsonify
from words import split_words

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/run")
def run_script():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    result = split_words(text)
    # return plain text so we can drop it right into a <pre>
    return "\n".join(result), 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.get("/healthz")
def health():
    return "ok", 200

if __name__ == "__main__":
    # Local dev: `python app.py`
    app.run(host="0.0.0.0", port=5000, debug=True)
