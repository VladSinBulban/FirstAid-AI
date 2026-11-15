
import unittest

from backend.triage import (
    assess_urgency,
    EMERGENCY,
    PROMPT_ASSESSMENT,
    LOWER_URGENCY,
)


class TestTriage(unittest.TestCase):

    def test_emergency_flag_takes_priority(self):
        result = assess_urgency(
            selected_red_flags={"severe_bleeding"},
            selected_urgent_flags={"cannot_bear_weight"},
            pain_level="Mild",
        )
        self.assertEqual(result["level"], EMERGENCY)

    def test_severe_pain_requires_prompt_assessment(self):
        result = assess_urgency(
            selected_red_flags=set(),
            selected_urgent_flags=set(),
            pain_level="Severe",
        )
        self.assertEqual(result["level"], PROMPT_ASSESSMENT)

    def test_urgent_flag_requires_prompt_assessment(self):
        result = assess_urgency(
            selected_red_flags=set(),
            selected_urgent_flags={"cannot_use_limb"},
            pain_level="Moderate",
        )
        self.assertEqual(result["level"], PROMPT_ASSESSMENT)

    def test_no_flags_returns_lower_urgency(self):
        result = assess_urgency(
            selected_red_flags=set(),
            selected_urgent_flags=set(),
            pain_level="Mild",
        )
        self.assertEqual(result["level"], LOWER_URGENCY)

    def test_emergency_cannot_be_downgraded(self):
        result = assess_urgency(
            selected_red_flags={"breathing_or_chest"},
            selected_urgent_flags=set(),
            pain_level="No pain",
        )
        self.assertNotEqual(result["level"], LOWER_URGENCY)


if __name__ == "__main__":
    unittest.main()
