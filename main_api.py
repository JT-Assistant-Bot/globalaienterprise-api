from flask import Flask, request, jsonify

from enforcement import check_and_increment
from webhook import handle_gumroad_webhook
from keys import get_key
from shield import shield_response

app = Flask(__name__)

# ================================
# 1. HEALTH CHECK
# ================================
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "running"}), 200


# ================================
# 2. PAID API MONITOR ENDPOINT
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
# 3. GUMROAD WEBHOOK ENDPOINT
# ================================
@app.route("/webhook/gumroad", methods=["POST"])
def gumroad_webhook():
    return handle_gumroad_webhook()


# ================================
# 4. API KEY RETRIEVAL ENDPOINT
# ================================
@app.route("/retrieve-key", methods=["POST"])
def retrieve_key():
    data = request.json or {}
    email = data.get("email")
    license_key = data.get("license_key")

    if not email or not license_key:
        return jsonify({"error": "email and license_key required"}), 400

    record = get_key(email, license_key)

    if not record:
        return jsonify({"error": "No key found"}), 404

    return jsonify(
        {
            "api_key": record["api_key"],
            "credits": record["credits"]
        }
    ), 200


# ================================
# 5. SHIELD CHECK ENDPOINT (PAID)
# ================================
@app.route("/shield/check", methods=["GET"])
def shield_check():
    api_key = request.headers.get("X-API-Key")

    allowed, message = shield_response(api_key)

    if not allowed:
        # unpaid or rate-limited
        status = 403 if "paid" in message.lower() else 429
        return jsonify({"error": message}), status

    return jsonify({"decision": "allow"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
