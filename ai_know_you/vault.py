"""Local, zero-knowledge encrypted vault for the profile directory.

The vault uses AES-256-CBC with a key derived from a passphrase via
PBKDF2-HMAC-SHA256, plus an HMAC-SHA256 over salt+IV+ciphertext for integrity.
All cryptography is bundled into the profile directory as a single ``.akyv``
file; on unseal the archive is restored in place.

This module is **optional**: it imports ``pyaes`` lazily so the rest of the
tool works without it. Install with ``pip install ai-know-you[crypto]``.
"""

from __future__ import annotations

import hmac
import io
import os
import tarfile
from typing import Optional

try:
    import pyaes  # type: ignore
    _HAS_PYAES = True
except Exception:  # pragma: no cover - optional dependency
    _HAS_PYAES = False

PBKDF2_ITERS = 200_000
SALT_LEN = 16
IV_LEN = 16
HMAC_LEN = 32
_MAGIC = b"AKYV1\x00"


def _require() -> None:
    if not _HAS_PYAES:
        raise RuntimeError(
            "the vault needs the 'pyaes' package. Install it with: "
            "pip install ai-know-you[crypto]"
        )


def _derive(passphrase: str, salt: bytes) -> tuple[bytes, bytes]:
    dk = hashlib_pbkdf2(passphrase, salt)
    return dk[:32], dk[32:]


def hashlib_pbkdf2(passphrase: str, salt: bytes) -> bytes:
    import hashlib

    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, PBKDF2_ITERS, dklen=64)


def _pkcs7_pad(data: bytes, block: int = 16) -> bytes:
    pad = block - (len(data) % block)
    return data + bytes([pad]) * pad


def _pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("empty payload")
    pad = data[-1]
    if pad < 1 or pad > 16:
        raise ValueError("bad padding")
    return data[:-pad]


def _aes_cbc(key: bytes, iv: bytes, data: bytes, decrypt: bool) -> bytes:
    aes = pyaes.AESModeOfOperationCBC(key, iv)
    out = b""
    for i in range(0, len(data), 16):
        block = data[i : i + 16]
        out += aes.decrypt(block) if decrypt else aes.encrypt(block)
    return out


def seal(directory: str, passphrase: str, vault_path: str) -> str:
    """Pack ``directory`` into an encrypted ``.akyv`` vault at ``vault_path``."""
    _require()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(directory, arcname=".")
    plain = buf.getvalue()

    salt = os.urandom(SALT_LEN)
    iv = os.urandom(IV_LEN)
    aes_key, hmac_key = _derive(passphrase, salt)
    ct = _aes_cbc(aes_key, iv, _pkcs7_pad(plain), decrypt=False)
    mac = hmac.new(hmac_key, salt + iv + ct, "sha256").digest()
    blob = _MAGIC + salt + iv + ct + mac

    with open(vault_path, "wb") as fh:
        fh.write(blob)
    return vault_path


def unseal(vault_path: str, passphrase: str, out_directory: str) -> str:
    """Verify and restore an ``.akyv`` vault into ``out_directory``."""
    _require()
    with open(vault_path, "rb") as fh:
        raw = fh.read()
    if raw[: len(_MAGIC)] != _MAGIC:
        raise ValueError("not an ai-know-you vault file")
    blob = raw[len(_MAGIC):]
    salt, iv = blob[:SALT_LEN], blob[SALT_LEN : SALT_LEN + IV_LEN]
    ct, mac = blob[SALT_LEN + IV_LEN : -HMAC_LEN], blob[-HMAC_LEN:]
    aes_key, hmac_key = _derive(passphrase, salt)
    expected = hmac.new(hmac_key, salt + iv + ct, "sha256").digest()
    if not hmac.compare_digest(expected, mac):
        raise ValueError("wrong passphrase or corrupted vault")
    plain = _pkcs7_unpad(_aes_cbc(aes_key, iv, ct, decrypt=True))

    os.makedirs(out_directory, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(plain), mode="r:gz") as tar:
        tar.extractall(out_directory)
    return out_directory
