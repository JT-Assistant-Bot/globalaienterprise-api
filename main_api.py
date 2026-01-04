from flask import Flask, request, jsonify

from enforcement import check_and_increment
from webhook import handle_gumroad_webhook

app = Flask(__name__)

# ================================
# 1. PAID API MONITOR ENDPOINT
# ================================
@app.route("/monitor/check", methods=["GET"])
def monitor_check():
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        return jsonify({"error": "API key missing"}), 401

    if not check_and_increment(api_key):
        return jsonify({"error": "API key missing or invalid"}), 401

    return jsonify({"status": "ok"}), 200


# ================================
# 2. GUMROAD WEBHOOK ENDPOINT
# ================================
@app.route("/webhook/gumroad", methods=["POST"])
def gumroad_webhook():
    return handle_gumroad_webhook()


# ================================
# 3. HEALTH CHECK (OPTIONAL)
# ================================
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
