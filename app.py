import logging
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from chatbot.chatbot_engine import get_response


PROJECT_DIR = Path(__file__).resolve().parent
DATABASE_DIR = PROJECT_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "chatbot.db"
MAX_MESSAGE_LENGTH = 2000

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Open a connection to the local chat database."""
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the database directory and chat table when the app starts."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/history", methods=["GET"])
def history():
    try:
        with get_db_connection() as connection:
            rows = connection.execute(
                """
                SELECT user_message, bot_response,
                       strftime('%Y-%m-%dT%H:%M:%fZ', created_at) AS created_at
                FROM conversations
                ORDER BY id DESC
                LIMIT 100
                """
            ).fetchall()
        messages = []
        for row in reversed(rows):
            messages.extend(
                [
                    {
                        "role": "user",
                        "text": row["user_message"],
                        "time": row["created_at"],
                    },
                    {
                        "role": "assistant",
                        "text": row["bot_response"],
                        "time": row["created_at"],
                    },
                ]
            )
        return jsonify({"messages": messages})
    except sqlite3.Error:
        logger.exception("Could not load chat history")
        return jsonify({"error": "Chat history is temporarily unavailable."}), 500


@app.route("/chat", methods=["POST", "DELETE"])
def chat():
    if request.method == "DELETE":
        try:
            with get_db_connection() as connection:
                connection.execute("DELETE FROM conversations")
            return jsonify({"message": "Chat history cleared."})
        except sqlite3.Error:
            logger.exception("Could not clear chat history")
            return jsonify({"error": "Chat history could not be cleared. Please try again."}), 500

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Please send your message as JSON."}), 400

    user_message = data.get("message")
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "Please type a message before sending."}), 400

    user_message = user_message.strip()
    if len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": "Messages must be 2000 characters or fewer."}), 400

    try:
        bot_response = get_response(user_message)
    except Exception:
        logger.exception("Unexpected error while generating a chat response")
        return jsonify(
            {"error": "Sorry, something went wrong while creating a reply. Please try again."}
        ), 500

    try:
        with get_db_connection() as connection:
            connection.execute(
                "INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)",
                (user_message, bot_response),
            )
    except sqlite3.Error:
        logger.exception("Could not save the conversation")
        return jsonify(
            {"error": "Your message could not be saved. Please try again."}
        ), 500

    return jsonify({"reply": bot_response})


@app.errorhandler(500)
def internal_server_error(_error):
    if request.path in {"/chat", "/history"}:
        return jsonify({"error": "Sorry, a server error occurred. Please try again."}), 500
    return "Sorry, a server error occurred. Please try again.", 500


if __name__ == "__main__":
    app.run(debug=False)
