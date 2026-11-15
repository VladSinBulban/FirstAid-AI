"""Basic output checks for the prototype's final AI summary.

This is a narrow safeguard, not a comprehensive medical-content filter.
"""
import re


BLOCKED_PATTERNS = (
    r"\b(ibuprofen|paracetamol|acetaminophen|aspirin|naproxen|"
    r"diclofenac|medication dose|take \d+ ?mg)\b",
    r"\b(compression wrap|compress the area|elevate the (?:leg|arm|injured area))\b",
    r"\b(you (?:definitely |probably |likely )?have a "
    r"(?:fracture|sprain|strain|dislocation|concussion))\b",
    r"\b(nothing to worry about|definitely fine|not serious|"
    r"no need to (?:see|get) (?:a )?(?:doctor|medical help))\b",
)


def validate_ai_response(response: str) -> tuple[bool, str]:
    """Reject a small set of unsafe or incomplete response patterns."""
    if not response or not response.strip():
        return False, "empty_response"

    text = response.strip()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "blocked_medical_content"

    if "?" in text:
        return False, "unexpected_follow_up_question"

    if text[-1] not in ".!?)]*`":
        return False, "possibly_incomplete_response"

    return True, "ok"
