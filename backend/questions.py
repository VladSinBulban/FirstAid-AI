"""Focused follow-up questions. These collect context; they do not diagnose."""

QUESTION_BANK = {
    "tailbone_pelvis": [
        {
            "id": "leg_weakness",
            "question": "Since the fall, have you noticed any new weakness or loss of movement in either leg?",
        },
        {
            "id": "leg_numbness",
            "question": "Have you noticed any new numbness or tingling in either leg?",
        },
        {
            "id": "walking_ability",
            "question": "Can you stand and walk, or does putting weight on your legs cause significant pain?",
        },
        {
            "id": "head_neck_impact",
            "question": "Did you also hit your head or neck?",
        },
        {
            "id": "loss_consciousness",
            "question": "Did you lose consciousness at any point after the fall?",
        },
    ],
    "knee": [
        {
            "id": "weight_bearing",
            "question": "Can you put weight on that leg and take a few steps?",
        },
        {
            "id": "knee_swelling",
            "question": "Did the knee swell quickly or become visibly misshapen?",
        },
        {
            "id": "knee_movement",
            "question": "Can you gently bend and straighten the knee, or does it feel locked?",
        },
    ],
    "ankle_foot": [
        {
            "id": "weight_bearing",
            "question": "Can you put weight on that foot and take a few steps?",
        },
        {
            "id": "foot_swelling",
            "question": "Did the ankle or foot swell quickly or become visibly misshapen?",
        },
        {
            "id": "sensation",
            "question": "Do you have any new numbness, tingling, or unusual coldness in that foot?",
        },
    ],
    "arm_hand": [
        {
            "id": "arm_use",
            "question": "Can you use the arm and move your fingers normally?",
        },
        {
            "id": "arm_deformity",
            "question": "Is there major swelling or an obvious change in the shape of the arm or wrist?",
        },
        {
            "id": "arm_sensation",
            "question": "Do you have any new numbness, tingling, or unusual coldness in that hand?",
        },
    ],
    "shoulder": [
        {
            "id": "arm_movement",
            "question": "Can you move the arm gently, or is movement very painful or restricted?",
        },
        {
            "id": "shoulder_shape",
            "question": "Does the shoulder look visibly different from the other side?",
        },
        {
            "id": "arm_sensation",
            "question": "Do you have any new numbness, tingling, or weakness in that arm or hand?",
        },
    ],
    "head_neck_back": [
        {
            "id": "neurological_symptoms",
            "question": "Have you noticed new weakness, numbness, tingling, confusion, or problems with balance since the injury?",
        },
        {
            "id": "loss_consciousness",
            "question": "Did you lose consciousness, have a seizure, or vomit repeatedly after the injury?",
        },
        {
            "id": "pain_severity",
            "question": "Is the pain severe or getting worse?",
        },
    ],
    "general": [
        {
            "id": "location",
            "question": "Where exactly is the pain, and what part of your body was injured?",
        },
        {
            "id": "function",
            "question": "What movement or normal activity is difficult because of the injury?",
        },
        {
            "id": "symptom_change",
            "question": "Are the symptoms getting worse, staying the same, or improving?",
        },
    ],
}


def get_next_question(injury_area: str, asked_question_ids: set[str]) -> dict | None:
    """Return the next unanswered area-specific question."""
    questions = QUESTION_BANK.get(injury_area, QUESTION_BANK["general"])

    for question in questions:
        if question["id"] not in asked_question_ids:
            return question

    return None
