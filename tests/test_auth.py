from datetime import datetime, timedelta, timezone
import jwt
import pytest

from security import ALGORITHM, SECRET_KEY, hash_password, verify_password



USER = {"username": "student", "email": "student@example.com", "password": "secret123"}

def test_password_hash():
    hashed = hash_password(USER["password"])
    assert hashed != USER["password"]
    assert verify_password(USER["password"], hashed)
    assert not verify_password("wrong", hashed)


def test_login_and_profile(client):
    registered = client.post("/auth/register", json=USER)
    assert registered.status_code == 201
    assert set(registered.json()) == {"id", "username", "email"}
    login = client.post("/auth/login", json=USER)
    assert login.status_code == 200
    token = login.json()["access_token"]
    profile = client.get("/profile/me", headers={"Authorization": f"Bearer {token}"})
    assert profile.status_code == 200
    assert profile.json() == registered.json()


def test_profile_requires_token(client):
    response = client.get("/profile/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_duplicate_registration(client):
    registered = client.post("/auth/register", json=USER)
    if registered.status_code == 201:
        registered = client.post("/auth/register", json=USER)
        assert registered.status_code == 409


@pytest.mark.parametrize("body", [USER, {**USER, "password": "wrong"}])
def test_bad_login(client, body):
    if body["password"] == "wrong":
        client.post("/auth/register", json=USER)
    assert client.post("/auth/login", json=body).status_code == 401


def test_invalid_registration(client):
    assert client.post("/auth/register", json={**USER, "email": "invalid"}).status_code == 422


@pytest.mark.parametrize("kind", ["missing", "invalid", "expired", "no-expiry", "unknown-user", "bad-signature"])
def test_reject_token(client, kind):
    client.post("/auth/register", json=USER)
    payload = {"sub": USER["email"], "exp": datetime.now(timezone.utc) + timedelta(minutes=10)}
    if kind == "expired":
        payload["exp"] = datetime(2000, 1, 1, tzinfo=timezone.utc)
    if kind == "no-expiry":
        del payload["exp"]
    if kind == "unknown-user":
        payload["sub"] = "unknown@example.com"
    key = "other-test-signing-key-12345678901234567890" if kind == "bad-signature" else SECRET_KEY
    token = "invalid" if kind == "invalid" else jwt.encode(payload, key, algorithm=ALGORITHM)
    headers = {} if kind == "missing" else {"Authorization": f"Bearer {token}"}
    assert client.get("/profile/me", headers=headers).status_code == 401