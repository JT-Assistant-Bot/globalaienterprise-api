# GlobalAIEnterprise Shield API

GlobalAIEnterprise Shield is a machine-to-machine abuse and rate-limit guard for HTTP APIs.

It is designed to be called before your own API logic.
If the request is allowed, your API continues.
If the request is blocked, your API stops.

No SDK. No setup. One HTTP call.

🔒 **Paid Access Required**

Purchase API access:
https://jathangkip.gumroad.com/l/vtagec

You will receive an API key immediately after purchase.
Requests without a valid key are automatically blocked.

---

## Core Rule

Every request to your API must first call this endpoint:

```
GET /shield/check
```

If the response status is:
- 200 → allow request
- anything else → block request

---

## Authentication

Every request must include this header:

```
X-API-Key: YOUR_API_KEY
```

---

## Complete Python Example

```python
import requests
from flask import Flask, jsonify

app = Flask(__name__)

SHIELD_URL = "https://YOUR_DEPLOYED_API_DOMAIN/shield/check"
API_KEY = "PASTE_YOUR_API_KEY_HERE"

def shield_allows():
    response = requests.get(
        SHIELD_URL,
        headers={"X-API-Key": API_KEY},
        timeout=3
    )
    return response.status_code == 200

@app.route("/my-api")
def my_api():
    if not shield_allows():
        return jsonify({"error": "blocked or rate limited"}), 429

    return jsonify({
        "status": "ok",
        "data": "your real api logic runs here"
    })

if __name__ == "__main__":
    app.run()
```

---

## Complete Node.js Example

```js
import express from "express";
import fetch from "node-fetch";

const app = express();

const SHIELD_URL = "https://YOUR_DEPLOYED_API_DOMAIN/shield/check";
const API_KEY = "PASTE_YOUR_API_KEY_HERE";

async function shieldAllows() {
  const response = await fetch(SHIELD_URL, {
    headers: { "X-API-Key": API_KEY }
  });
  return response.status === 200;
}

app.get("/my-api", async (req, res) => {
  if (!(await shieldAllows())) {
    return res.status(429).json({ error: "blocked or rate limited" });
  }

  res.json({
    status: "ok",
    data: "your real api logic runs here"
  });
});

app.listen(3000);
```

---

## Response Codes

| Status | Meaning |
|------|--------|
| 200 | Request allowed |
| 401 | Invalid or missing API key |
| 429 | Rate limit exceeded |
| 403 | Access blocked |

---

## Usage Rules

- One API key per client
- Each request consumes credits
- Abuse is automatically blocked
- No interpretation or analytics are provided

---

## Infrastructure Notice

This service is infrastructure.

If you remove this call, your API loses protection.
That decision is entirely yours.
