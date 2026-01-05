from flask import Flask, request, jsonify
from datetime import datetime

from enforcement import check_and_increment

app = Flask(__name__)

# -------------------------
# In-memory free usage tracker
# -------------------------
FREE_LIMIT_PER_DAY = 50
_free_usage = {}  # { ip: { "date": "YYYY-MM-DD", "count": int } }


# -------------------------
# Helpers
# -------------------------
def _today():
    return datetime.utcnow().strftime("%Y-%m-%d")


def _get_client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)


# -------------------------
# Health Check
# -------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# -------------------------
# FREE MACHINE ENDPOINT
# -------------------------
@app.route("/free/validate", methods=["GET"])
def free_validate():
    ip = _get_client_ip()
    today = _today()

    record = _free_usage.get(ip)

    if not record or record["date"] != today:
        record = {"date": today, "count": 0}
        _free_usage[ip] = record

    if record["count"] >= FREE_LIMIT_PER_DAY:
        return (
            jsonify(
                {
                    "error": "Free limit reached",
                    "message": "Upgrade required to continue usage.",
                    "upgrade_url": "https://jathangkip.gumroad.com/l/vtagec",
                }
            ),
            402,
        )

    record["count"] += 1

    return (
        jsonify(
            {
                "status": "ok",
                "remaining": FREE_LIMIT_PER_DAY - record["count"],
            }
        ),
        200,
    )


# -------------------------
# PAID SHIELD ENDPOINT
# -------------------------
@app.route("/shield/check", methods=["GET"])
def shield_check():
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        return jsonify(
            {
                "error": "Missing API key",
                "decision": "deny",
            }
        ), 403

    allowed = check_and_increment(api_key)

    if not allowed:
        return jsonify(
            {
                "error": "Access denied. This endpoint requires a paid API key.",
                "decision": "deny",
            }
        ), 403

    return jsonify({"decision": "allow"}), 200


# -------------------------
# App Entrypoint
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
