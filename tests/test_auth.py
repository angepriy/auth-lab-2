"""
Test Suite: Authentication API
===============================
10 tests that cover the /login endpoint.
The CI pipeline runs these and the score is based on how many pass.
"""

import pytest
import json
import sys
import os

# Make sure the app module is importable from the repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ── Health / Smoke Tests ────────────────────────────────────────────────────

def test_health_endpoint(client):
    """The /health endpoint should return 200."""
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_returns_json(client):
    """The /health endpoint should return valid JSON."""
    resp = client.get("/health")
    data = json.loads(resp.data)
    assert "status" in data


# ── Login – Happy Path ──────────────────────────────────────────────────────

def test_login_valid_credentials_returns_200(client):
    """POST /login with valid creds should return 200."""
    resp = client.post(
        "/login",
        json={"username": "student", "password": "secret"},
    )
    assert resp.status_code == 200


def test_login_valid_credentials_returns_token(client):
    """Response body must contain a 'token' key."""
    resp = client.post(
        "/login",
        json={"username": "student", "password": "secret"},
    )
    data = json.loads(resp.data)
    assert "token" in data


def test_login_token_is_non_empty(client):
    """The token value must not be empty."""
    resp = client.post(
        "/login",
        json={"username": "student", "password": "secret"},
    )
    data = json.loads(resp.data)
    assert data["token"]


def test_login_accepts_content_type_json(client):
    """Endpoint must accept application/json."""
    resp = client.post(
        "/login",
        data=json.dumps({"username": "student", "password": "secret"}),
        content_type="application/json",
    )
    assert resp.status_code == 200


# ── Login – Error Cases ─────────────────────────────────────────────────────

def test_login_wrong_password_returns_401(client):
    """Wrong password must return 401 Unauthorized."""
    resp = client.post(
        "/login",
        json={"username": "student", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_login_wrong_username_returns_401(client):
    """Unknown username must return 401."""
    resp = client.post(
        "/login",
        json={"username": "hacker", "password": "secret"},
    )
    assert resp.status_code == 401


def test_login_missing_body_does_not_crash(client):
    """Empty body should return 4xx, not 500."""
    resp = client.post("/login", json={})
    assert resp.status_code in (400, 401, 422)


def test_login_returns_json_on_error(client):
    """Error response should still be JSON."""
    resp = client.post(
        "/login",
        json={"username": "bad", "password": "bad"},
    )
    # Should be parseable JSON
    data = json.loads(resp.data)
    assert isinstance(data, dict)
