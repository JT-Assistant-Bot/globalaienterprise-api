"""
main_api.py
Primary entrypoint for GlobalAIEnterprise API.
"""

from flask import Flask, request, jsonify
from enforcement import check_and_increment

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/shield/check", methods=["GET"])
def shield_check():
    api_key = request.headers.get("X-API-Key")

    allowed = check_and_increment(api_key)

    if not allowed:
        return (
            jsonify(
                {
                    "error": "Access denied. This endpoint requires a paid API key.",
                    "decision": "deny",
                }
            ),
            403,
        )

    return jsonify({"decision": "allow"}), 200


if __name__ == "__main__":
    # Railway sets PORT automatically
    app.run(host="0.0.0.0", port=8080)
