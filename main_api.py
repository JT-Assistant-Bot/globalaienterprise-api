# main_api.py

from flask import Flask, request, jsonify
import requests
import hashlib
import time

from auth import validate_request, AuthError

app = Flask(__name__)


@app.route("/monitor/check", methods=["GET"])
def monitor_check():
    try:
        # Enforce API key + rate limit
        validate_request(request.headers)

        url = request.args.get("url")
        if not url:
            return jsonify({"error": "Missing url parameter"}), 400

        start_time = time.time()

        response = requests.get(url, timeout=5)

        response_time_ms = int((time.time() - start_time) * 1000)
        content_hash = hashlib.sha1(response.content).hexdigest()

        return jsonify({
            "url": url,
            "status_code": response.status_code,
            "reachable": True,
            "response_time_ms": response_time_ms,
            "content_hash": content_hash
        })

    except AuthError as e:
        return jsonify({"error": str(e)}), 401

    except requests.exceptions.RequestException:
        return jsonify({
            "url": request.args.get("url"),
            "reachable": False
        }), 200

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
