"""Privacy-first field handling.

ai-know-you is local-first by design. On top of that, a set of sensitive
categories is *never* persisted to the profile. When a user answer looks like
it touches one of these categories we redact it before storage and emit a
clear notice instead of silently keeping it.
"""

from __future__ import annotations

import re

# Categories that must never be written into the profile.
SENSITIVE_CATEGORIES = {
    "credential": ["password", "token", "secret", "api key", "access key", "private key"],
    "identity_doc": ["id card", "passport", "social security", "身份证", "护照"],
    "financial": ["bank account", "card number", "cvv", "银行卡", "信用卡"],
    "health": ["medical", "diagnosis", "health record", "病历", "诊断"],
    "location_precise": ["home address", "gps", "家庭住址"],
}

# Loose detectors. Deliberately conservative: false positives only cause a
# prompt, not data loss.
_PATTERNS = {
    "credential": re.compile(r"(?i)(password|token|secret|api[_ ]?key|private[_ ]?key)"),
    "identity_doc": re.compile(r"(?i)(\b\d{6,}\b.*(id|passport)|身份证|护照)"),
    "financial": re.compile(r"(?i)(\b\d{12,}\b|cvv|银行卡|信用卡)"),
    "health": re.compile(r"(?i)(medical|diagnosis|病历|诊断)"),
}


def detect_sensitive(text: str) -> list[str]:
    """Return the list of sensitive categories a piece of text appears to hit."""
    hits: list[str] = []
    for category, pattern in _PATTERNS.items():
        if pattern.search(text or ""):
            hits.append(category)
    return hits


def is_sensitive(text: str) -> bool:
    return bool(detect_sensitive(text))


def redact(text: str) -> str:
    """Replace the middle of a sensitive value with asterisks, keeping length hint."""
    text = (text or "").strip()
    if len(text) <= 4:
        return "****"
    return text[:2] + "*" * max(4, len(text) - 4) + text[-2:]
