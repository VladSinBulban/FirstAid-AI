
"""Reviewed first-aid guidance for the FirstAid AI prototype.

The guidance is educational and conservative. It is not a diagnosis
or a substitute for professional medical assessment.

Sources:
- 2024 AHA / American Red Cross First Aid Guidelines
- NHS Sprains and Strains guidance
"""

GUIDANCE_VERSION = "1.0"
GUIDANCE_STATUS = "SOURCE_BASED_PROTOTYPE_NOT_CLINICALLY_VALIDATED"

EMERGENCY_GUIDANCE = {
    "title": "Emergency — get help now",
    "instructions": [
        "Call 112 in Romania, or ask someone nearby to call.",
        "Get a trusted adult immediately.",
        "Do not wait for this application to provide further advice.",
        "Avoid unnecessary movement of the injured area.",
        "Follow the emergency operator's instructions.",
    ],
}

FIRST_AID_GUIDANCE = {
    "soft_tissue": {
        "title": "Initial care for a painful soft-tissue injury",
        "instructions": [
            "Stop the activity that caused the pain.",
            "Avoid activities that cause pain or require using the injured area.",
            "Keep the injured area supported in a comfortable position.",
            "A cold pack wrapped in a damp cloth may help with pain and swelling.",
            "Limit each cold application to 20–30 minutes. Never apply ice directly to skin.",
            "Seek medical assessment if the injury limits normal use or symptoms are severe or worsening.",
        ],
        "source": "AHA / American Red Cross 2024 First Aid Guidelines",
        "source_url": (
            "https://cpr.heart.org/en/resuscitation-science/"
            "2024-first-aid-guidelines"
        ),
    },

    "suspected_fracture": {
        "title": "Possible fracture — protect the injured area",
        "instructions": [
            "Stop the activity and avoid using the injured limb.",
            "Keep the injured area supported in the position you found it.",
            "Do not attempt to straighten the limb or put a joint back into place.",
            "Do not push a visible bone back into a wound.",
            "Get medical assessment promptly.",
            "If the limb is blue, very pale, cold, or numb, or looks badly deformed, call 112.",
        ],
        "source": "AHA / American Red Cross 2024 First Aid Guidelines",
        "source_url": (
            "https://cpr.heart.org/en/resuscitation-science/"
            "2024-first-aid-guidelines"
        ),
    },

    "head_neck_back": {
        "title": "Head, neck or back injury",
        "instructions": [
            "Stop the activity.",
            "If a serious head, neck, or back injury is suspected, call 112.",
            "Encourage the injured person to remain as still as possible.",
            "Do not unnecessarily move their head, neck, or back.",
            "Stay with the person if it is safe to do so.",
            "Follow the emergency operator's instructions.",
        ],
        "source": "AHA / American Red Cross 2024 First Aid Guidelines",
        "source_url": (
            "https://cpr.heart.org/en/resuscitation-science/"
            "2024-first-aid-guidelines"
        ),
    },

    "minor_wound": {
        "title": "Minor wound",
        "instructions": [
            "Stop the activity and avoid further injury.",
            "If the wound is bleeding heavily or bleeding will not stop, call 112.",
            "For a wound associated with a suspected fracture, seek medical help.",
            "Do not attempt to remove an embedded object.",
            "Ask a trusted adult for help assessing the wound.",
        ],
        "source": "AHA / American Red Cross 2024 First Aid Guidelines",
        "source_url": (
            "https://cpr.heart.org/en/resuscitation-science/"
            "2024-first-aid-guidelines"
        ),
    },
}

GENERAL_GUIDANCE = {
    "title": "General injury precautions",
    "instructions": [
        "Stop activities that cause pain.",
        "Avoid putting unnecessary strain on the injured area.",
        "Tell a trusted adult what happened.",
        "Seek medical advice if symptoms persist, worsen, or concern you.",
        "If you are unsure how serious the injury is, choose medical assessment.",
    ],
    "source": "General conservative prototype guidance",
    "source_url": None,
}


def get_first_aid_guidance(
    guidance_key: str,
    emergency: bool = False,
) -> dict:
    """Return guidance without allowing emergency cases to be downgraded."""

    if emergency:
        return {
            **EMERGENCY_GUIDANCE,
            "status": GUIDANCE_STATUS,
            "version": GUIDANCE_VERSION,
            "is_emergency": True,
        }

    guidance = FIRST_AID_GUIDANCE.get(
        guidance_key,
        GENERAL_GUIDANCE,
    )

    return {
        **guidance,
        "status": GUIDANCE_STATUS,
        "version": GUIDANCE_VERSION,
        "is_emergency": False,
    }
