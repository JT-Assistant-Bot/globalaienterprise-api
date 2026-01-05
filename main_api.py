from flask import Flask, request, jsonify

from enforcement import check_and_increment
from webhook import handle_gumroad_webhook

app = Flask(__name__)

# -------------------------
# Health Check
# -------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# -------------------------
# Shield Check (Paid Gate)
# -------------------------
@app.route("/shield/check", methods=["GET"])
def shield_check():
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        return jsonify({
            "error": "Missing API key",
            "decision": "deny"
        }), 403

    allowed = check_and_increment(api_key)

    if not allowed:
        return jsonify({
            "error": "Access denied. This endpoint requires a paid API key.",
            "decision": "deny"
        }), 403

    return jsonify({"decision": "allow"}), 200


# -------------------------
# Gumroad Webhook
# -------------------------
@app.route("/webhook/gumroad", methods=["POST"])
def gumroad_webhook():
    try:
        return handle_gumroad_webhook()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------
# App Entrypoint
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
