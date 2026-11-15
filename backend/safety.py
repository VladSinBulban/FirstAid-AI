
EMERGENCY_FLAGS = {
    "severe_bleeding": "Severe bleeding that will not stop",
    "visible_bone": "Bone visible through a wound",
    "major_deformity": "The injured limb or joint looks badly deformed",
    "circulation_or_sensation": "Fingers or toes are blue, very pale, cold, or numb",
    "altered_consciousness": "Unconsciousness, confusion, seizure, or difficulty staying awake",
    "breathing_or_chest": "Trouble breathing or chest pain",
    "serious_head_neck_back": "Serious head, neck, or back injury",
}


def check_emergency_flags(selected_flags: set[str]) -> list[str]:
    """Return selected emergency warning sign IDs."""
    return [
        flag_id
        for flag_id in EMERGENCY_FLAGS
        if flag_id in selected_flags
    ]


def has_emergency_flags(selected_flags: set[str]) -> bool:
    return bool(check_emergency_flags(selected_flags))
