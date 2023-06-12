from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def testing():
    return make_response(jsonify({"Test":"OK"}), 200)
