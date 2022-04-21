from flask import Flask, request, Response
from flask_expects_json import expects_json
from pathlib import Path

from src.DatabaseManager import DatabaseManager

app = Flask(__name__)
database_manager = None

SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "paragraphs": {
            "type": "array",
            "items": [
                {
                    "type": "string"
                }
            ]
        }
    },
    "required": [
        "title",
        "paragraphs"
    ]
}

@app.route("/post", methods=["POST"])
@expects_json(SCHEMA)
def post():
    content = request.json
    database_manager.insert_post(content["title"], content["paragraphs"])
    return Response("{status:'Content posted successfully'}", status=200, mimetype="application/json")

class APIController:
    def __init__(self, host: str, port: str, database_path: Path):
        self.database_manager = DatabaseManager(database_path)
        global database_manager
        database_manager = self.database_manager
        self.app = app
        self.host = host
        self.port = port

    def start(self):
        app.run(self.host, self.port)
