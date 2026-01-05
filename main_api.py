from flask import Flask, request, jsonify
from enforcement import check_and_increment

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

PURCHASE_URL = "https://jathangkip.gumroad.com/l/vtagec"
FREE_QUOTA = 50

# -----------------------------
# HEALTH
# -----------------------------

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "service": "GlobalAIEnterprise Shield",
        "status": "online",
        "docs": "See README for usage"
    })

# -----------------------------
# SHIELD CHECK (PAID ACCESS)
# -----------------------------

@app.route("/shield/check", methods=["GET"])
def shield_check():
    api_key = request.headers.get("X-API-Key")
    decision = check_and_increment(api_key)

    if decision["allowed"]:
        return jsonify({"decision": "allow"}), 200

    return jsonify({
        "decision": "deny",
        "reason": decision["reason"],
        "upgrade": PURCHASE_URL
    }), 403

# -----------------------------
# FREE VALIDATION (DISCOVERY)
# -----------------------------

@app.route("/free/validate", methods=["GET"])
def free_validate():
    api_key = request.headers.get("X-API-Key")

    result = check_and_increment(
        api_key=api_key,
        free_only=True,
        free_quota=FREE_QUOTA
    )

    if result["allowed"]:
        return jsonify({
            "status": "ok",
            "remaining": result["remaining"]
        }), 200

    # Free quota exhausted → forced upgrade
    return jsonify({
        "error": "Free quota exhausted",
        "message": "Upgrade required to continue",
        "upgrade": PURCHASE_URL
    }), 402

# -----------------------------
# FORCED UPGRADE ENDPOINT
# -----------------------------

@app.route("/upgrade", methods=["GET"])
def upgrade():
    return jsonify({
        "error": "Payment required",
        "message": "This API requires a paid key",
        "benefit": "Unlimited access + enforcement + no rate limits",
        "purchase": PURCHASE_URL
    }), 402


# -----------------------------
# ENTRYPOINT
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
