"""
Lab: Authentication API
=======================
Your task: implement a working /login endpoint.

Requirements (these are tested by pytest):
  POST /login
    Body: {"username": "...", "password": "..."}
    Returns 200 + {"token": "<any-string>"} when credentials are valid
    Returns 401 when credentials are invalid

Valid credentials for this lab:
  username: "student"
  password: "secret"
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# ── TODO: implement this endpoint ──────────────────────────────────────────

@app.route("/login", methods=["POST"])
def login():
    """Return a token when credentials are correct, 401 otherwise."""
    # Replace this with your implementation
    return jsonify({"error": "Not implemented"}), 501


# ── Extra endpoints (already implemented – do not modify) ──────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/")
def index():
    return jsonify({"message": "Auth Lab API"})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
