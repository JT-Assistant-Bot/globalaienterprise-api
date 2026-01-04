# webhook.py

from flask import request, jsonify
from keys import create_paid_key

# Optional: set this later to your Gumroad product permalink
GUMROAD_PRODUCT_PERMALINK = ""  # leave empty for now


def handle_gumroad_webhook():
    """
    Handles Gumroad ping events.
    Issues a paid API key when a valid sale occurs.
    """

    data = request.form.to_dict()

    # Gumroad sends sale events via 'sale'
    if data.get("event") != "sale":
        return jsonify({"status": "ignored"}), 200

    # Optional safety check (can be enabled later)
    if GUMROAD_PRODUCT_PERMALINK:
        if data.get("product_permalink") != GUMROAD_PRODUCT_PERMALINK:
            return jsonify({"status": "wrong product"}), 200

    # Issue paid API key with 1000 credits
    api_key = create_paid_key(credits=1000)

    return jsonify({
        "status": "success",
        "api_key": api_key,
        "credits": 1000
    }), 200