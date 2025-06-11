from pathlib import Path
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.models import ChatMessage
from database.extension import db

message_bp = Blueprint('message_bp', __name__)

@message_bp.route("/get-messages", methods=["GET"])
@jwt_required()
def get_messages():
    try:
        user_id = get_jwt_identity()
        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp.asc()).all()
        print(messages)

        return jsonify([
            {
                "user_message": msg.user_message,
                "bot_message": msg.bot_response,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
