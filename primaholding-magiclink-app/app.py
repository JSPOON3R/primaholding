from flask import Flask, request, jsonify
import jwt
import datetime
from flask_cors import CORS  # To allow frontend requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

REST_KEY = "rk_DM3_7yAfHUziGWYKx7upJcxZWRTKX_aM"

@app.route('/generate-link', methods=['POST'])
def generate_link():
    data = request.get_json()
    session_id = data.get("sessionId")

    if not session_id:
        return jsonify({"error": "Missing sessionId"}), 400

    payload = {
        "space_id": "930",
        "name": "Customer",
        "email": "Customer@example.com",
        "can_host": True,
        "urls": ["https://demo.surfly.com/company/Primaholding/contract_demo.pdf"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }

    magic_link = jwt.encode(payload, REST_KEY, algorithm="HS256")
    space_url = f"https://webfuse.com/+primaholding/?magic_link={magic_link}&session_id={session_id}"

    return jsonify({"message": "Magic Link", "link": space_url})
