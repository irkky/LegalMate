from flask import Blueprint, jsonify

bp = Blueprint('health', __name__)

@bp.route('/')
def home():
    """Original root endpoint without modifications"""
    return jsonify({
        "message": "API is running. Use /documents endpoints."
    }), 200