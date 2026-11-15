
"""Deterministic emergency confirmation for the chat interface."""

def parse_emergency_confirmation(answer: str) -> bool | None:
    """
    Return:
        True  = user confirms an emergency warning sign.
        False = user explicitly denies the listed signs.
        None  = unclear answer; ask again.
    """

    normalized = answer.strip().lower()
    normalized = normalized.rstrip(".!? ")

    affirmative = {
        "yes",
        "yes i do",
        "yes i am",
        "i do",
        "i am",
        "one or more",
        "at least one",
        "some of them",
    }

    negative = {
        "no",
        "no i don't",
        "no i do not",
        "none",
        "none of those",
        "not experiencing any",
        "i don't have any",
        "i do not have any",
    }

    if normalized in affirmative:
        return True

    if normalized in negative:
        return False

    if normalized.startswith(("yes,", "yes ", "yes.")):
        return True

    if normalized.startswith(("no,", "no ")):
        return False

    return None


EMERGENCY_MESSAGE = """
🚨 **Please get emergency help now.**

Call **112 in Romania** (or your local emergency number). Get a
trusted adult immediately.

- Do not wait for this application or continue the AI conversation.
- Avoid unnecessary movement of the injured area.
- Follow the emergency operator's instructions.
"""
