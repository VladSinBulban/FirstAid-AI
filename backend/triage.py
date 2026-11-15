
from backend.safety import check_emergency_flags

EMERGENCY = "emergency"
PROMPT_ASSESSMENT = "prompt_assessment"
LOWER_URGENCY = "lower_urgency"


def assess_urgency(
    selected_red_flags: set[str],
    selected_urgent_flags: set[str],
    pain_level: str,
) -> dict:
    """Classify urgency using the prototype's fixed rules."""

    emergency_flags = check_emergency_flags(selected_red_flags)

    # Emergency warning signs always take priority.
    if emergency_flags:
        return {
            "level": EMERGENCY,
            "matched_flags": emergency_flags,
            "message": "Emergency warning signs selected. Get emergency help now.",
        }

    if selected_urgent_flags or pain_level == "Severe":
        return {
            "level": PROMPT_ASSESSMENT,
            "matched_flags": list(selected_urgent_flags),
            "message": "Prompt medical assessment is appropriate.",
        }

    return {
        "level": LOWER_URGENCY,
        "matched_flags": [],
        "message": (
            "No listed warning signs were selected. "
            "This does not rule out a serious injury."
        ),
    }
