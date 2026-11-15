"""Conservative, keyword-based safety screening for the FirstAid AI prototype.

This module is deliberately not a diagnostic or validated triage tool.
It identifies a small set of explicit phrases for escalation and otherwise
returns uncertainty rather than declaring an injury safe.
"""
import re
from typing import Any


AREA_PATTERNS = {
    "tailbone_pelvis": (
        r"\b(tailbone|coccyx|buttocks?|butt|ass|pelvis|hip|seat bones?)\b",
    ),
    "knee": (r"\b(knee|kneecap)\b",),
    "ankle_foot": (r"\b(ankle|foot|feet|heel|toes?)\b",),
    "arm_hand": (r"\b(arm|elbow|wrist|hand|finger|fingers)\b",),
    "shoulder": (r"\b(shoulder|collarbone)\b",),
    "head_neck_back": (
        r"\b(head|skull|neck|spine|back|lower back)\b",
    ),
}

EMERGENCY_PATTERNS = {
    "severe_bleeding": (
        r"\b(bleeding (?:won't|will not|doesn't) stop|"
        r"cannot stop (?:the )?bleeding|can't stop (?:the )?bleeding|"
        r"bleeding heavily|bleeding a lot|spurting blood|blood is spurting|"
        r"uncontrolled bleeding)\b",
    ),
    "breathing_or_chest": (
        r"\b(trouble breathing|difficulty breathing|can't breathe|"
        r"cannot breathe|shortness of breath|chest pain)\b",
    ),
    "altered_consciousness": (
        r"\b(unconscious|passed out|lost consciousness|having a seizure|"
        r"seizure|new confusion|can't stay awake|cannot stay awake)\b",
    ),
    "major_deformity_or_open_fracture": (
        r"\b(bone (?:is )?(?:sticking out|visible)|bone through (?:the )?skin|"
        r"limb (?:is )?badly deformed|joint (?:is )?badly deformed)\b",
    ),
    "circulation_compromise": (
        r"\b((?:fingers?|toes?|hand|foot|limb) (?:are|is) "
        r"(?:blue|very pale|cold) and (?:numb|tingling)|"
        r"(?:blue|very pale|cold) (?:fingers?|toes?|hand|foot)|"
        r"(?:fingers?|toes?|hand|foot|limb) (?:are|is) "
        r"(?:blue|very pale|cold))\b",
    ),
    "spinal_neurological_symptoms": (
        r"\b(can't move (?:my )?(?:legs?|feet)|cannot move (?:my )?(?:legs?|feet)|"
        r"can't feel (?:my )?(?:legs?|feet)|cannot feel (?:my )?(?:legs?|feet))\b",
        r"\b(after (?:the )?fall|since (?:the )?fall|after (?:the )?injury).{0,80}"
        r"\b(can't move (?:my )?(?:legs?|feet)|cannot move (?:my )?(?:legs?|feet)|"
        r"new weakness in (?:my )?legs?|weakness in (?:my )?legs?|"
        r"loss of movement in (?:my )?legs?|loss of bladder control|"
        r"loss of bowel control)\b",
    ),
    "sudden_vision_loss": (
        r"\b(suddenly (?:can't|cannot) see|lost (?:my )?vision|"
        r"vision (?:went black|suddenly disappeared)|blind in one eye)\b",
    ),
}

URGENT_PATTERNS = {
    "cannot_bear_weight": (
        r"\b(can't|cannot|unable to) (?:put weight|bear weight|stand or walk|"
        r"walk) (?:on|because of|due to)?\b",
        r"\b(can't walk|cannot walk|unable to walk|can't stand|cannot stand)\b",
    ),
    "severe_pain_after_injury": (
        r"\b(severe pain|extreme pain|hurt a lot|hurts a lot|hurt really badly|hurts really badly|"
        r"pain is unbearable|unbearable pain)\b",
    ),
    "fall_from_height": (
        r"\b(fell|falling|fall) (?:down )?(?:from )?(?:a|the) "
        r"(?:tree|roof|balcony|ladder)\b",
        r"\b(fell|fall) from (?:a )?(?:height|high place)\b",
        r"\b(climbing|climbed) (?:up )?(?:a |the )?tree.{0,50}\b(fell|fall)\b",
    ),
    "significant_swelling_or_deformity": (
        r"\b(rapidly swelling|swelling is getting worse|"
        r"large swelling|obvious deformity|looks out of place)\b",
    ),
    "head_injury_symptoms": (
        r"\b(hit my head|hit their head|head injury)\b",
    ),
}

NEGATION_PREFIX = re.compile(
    r"(?:\bno\b|\bnot\b|\bnever\b|\bwithout\b|\bdon't\b|\bdo not\b|\bdoesn't\b|\bdoes not\b)"
    r"(?:\s+\w+){0,4}\s*$",
    re.IGNORECASE,
)


def _matches_positive(text: str, patterns: tuple[str, ...]) -> bool:
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            prefix = text[max(0, match.start() - 45):match.start()]
            phrase = match.group(0).lower()
            is_explicit_inability = phrase.startswith(
                ("can't", "cannot", "unable to")
            )
            if NEGATION_PREFIX.search(prefix) and not is_explicit_inability:
                continue
            return True
    return False


def detect_injury_area(text: str) -> str:
    """Identify a likely body area from plain language; never diagnose."""
    for area, patterns in AREA_PATTERNS.items():
        if _matches_positive(text, patterns):
            return area
    return "general"


def analyze_message(text: str) -> dict[str, Any]:
    """Return explicit warning signs and likely injury area."""
    normalized = re.sub(r"\s+", " ", text.strip().lower())

    emergency_flags = [
        flag
        for flag, patterns in EMERGENCY_PATTERNS.items()
        if _matches_positive(normalized, patterns)
    ]

    urgent_flags = [
        flag
        for flag, patterns in URGENT_PATTERNS.items()
        if _matches_positive(normalized, patterns)
    ]

    # "I can't see" is ambiguous: it may mean the person cannot see
    # the injured area, or that their vision has changed.
    ambiguous_vision = bool(
        re.search(r"\b(i )?(can't|cannot) see\b", normalized)
        and "suddenly can't see" not in normalized
        and "suddenly cannot see" not in normalized
    )

    return {
        "injury_area": detect_injury_area(normalized),
        "emergency_flags": emergency_flags,
        "urgent_flags": urgent_flags,
        "ambiguous_vision": ambiguous_vision,
    }


def analyze_conversation(messages: list[dict[str, str]]) -> dict[str, Any]:
    """Analyze all user messages so a later answer cannot erase earlier context."""
    user_text = " ".join(
        message.get("content", "")
        for message in messages
        if message.get("role") == "user"
    )
    return analyze_message(user_text)
