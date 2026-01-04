# webhook.py

from flask import request, jsonify
from keys import create_paid_key

# Optional hard lock (can be set later)
GUMROAD_PRODUCT_PERMALINK = ""


def handle_gumroad_webhook():
    """
    Gumroad Ping handler.
    Issues and stores a paid API key tied to buyer email + license key.
    """

    data = request.form.to_dict()

    # Only handle successful sales
    if data.get("event") != "sale":
        return jsonify({"status": "ignored"}), 200

    # Optional product validation
    if GUMROAD_PRODUCT_PERMALINK:
        if data.get("product_permalink") != GUMROAD_PRODUCT_PERMALINK:
            return jsonify({"status": "wrong product"}), 200

    buyer_email = data.get("email")
    license_key = data.get("license_key")

    if not buyer_email or not license_key:
        return jsonify({"error": "Missing buyer identity"}), 400

    api_key = create_paid_key(
        credits=1000,
        email=buyer_email,
        license_key=license_key
    )

    return jsonify({
        "status": "success",
        "api_key": api_key
    }), 200
