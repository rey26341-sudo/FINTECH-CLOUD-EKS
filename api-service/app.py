import sys
import os

# Allow imports from the project root (routes/, blockchain/, config.py)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from routes.invoice import invoice_bp

app = Flask(__name__)
app.register_blueprint(invoice_bp)

@app.route("/")
def home():
    return "fintech API is running"

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
