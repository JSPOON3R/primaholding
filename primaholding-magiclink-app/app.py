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
    new_tab = data.get("newTab")
    space_id = data.get("spaceId")
    space_url = data.get("spaceUrl")

    if not session_id:
        return jsonify({"error": "Missing sessionId"}), 400

    if not new_tab:
        return jsonify({"error": "Missing newTab"}), 400

    if not space_id:
        return jsonify({"error": "Missing Space Id"}), 400

    if not space_url:
        return jsonify({"error": "Missing Space Url"}), 400

    payload = {
        "space_id": [space_id],
        "name": "Customer",
        "email": "Customer@example.com",
        "can_host": True,
        "urls": [new_tab],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }

    magic_link = jwt.encode(payload, REST_KEY, algorithm="HS256")
    magic_url = f"{space_url}?magic_link={magic_link}&session_id={session_id}"

    return jsonify({"message": "Magic Link", "link": magic_url})
