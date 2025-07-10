from flask import Flask, request, jsonify
import jwt
import datetime
import logging
from flask_cors import CORS  # To allow frontend requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REST_KEY = "rk_JNGntDbpA_jVrCKD1Zwu1ro8amZYE_fU"

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
        "space_id": space_id,
        "name": "Customer",
        "email": "Customer@example.com",
        "can_host": True,
        "urls": [new_tab], #formatted as a list []
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }

    logger.info("JWT payload: %s", payload)

    magic_link = jwt.encode(payload, REST_KEY, algorithm="HS256")
    magic_url = f"{space_url}?magic_link={magic_link}" 
    #&session_id={session_id}

    logger.info("Magic URL: %s", magic_url)
    return jsonify({"message": "Magic Link", "link": magic_url})
