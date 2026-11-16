from src.users.infrastructure.argon2_password_hasher import (
    Argon2PasswordHasher,
)


def test_argon2_password_hasher_hashes_password():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash(
        "super-secret"
    )

    assert password_hash != "super-secret"


def test_argon2_password_hasher_verifies_correct_password():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash(
        "super-secret"
    )

    assert hasher.verify(
        "super-secret",
        password_hash,
    ) is True


def test_argon2_password_hasher_rejects_wrong_password():
    hasher = Argon2PasswordHasher()

    password_hash = hasher.hash(
        "super-secret"
    )

    assert hasher.verify(
        "wrong-password",
        password_hash,
    ) is False