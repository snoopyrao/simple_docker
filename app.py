from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
CHAT_FILE = os.path.join(OUTPUT_DIR, "chat_history.txt")

def append_to_chat_file(text: str):
    """Append chat text with timestamp to a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")

def read_chat_file() -> str:
    """Read the chat history file contents."""
    if not os.path.exists(CHAT_FILE):
        return "No chat history yet."
    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/run")
def run_script():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return "No input provided", 400

    # Save input to file
    append_to_chat_file(text)

    # Return output (each word on a new line)
    words = [w for w in text.split() if w]
    return "\n".join(words), 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.get("/view")
def view_output():
    """View saved chat history."""
    content = read_chat_file()
    return f"<h2>Saved Chat History</h2><pre>{content}</pre>"

@app.get("/healthz")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
