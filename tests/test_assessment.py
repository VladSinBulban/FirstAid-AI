import unittest
from backend.assessment import analyze_message, analyze_conversation


class TestAssessment(unittest.TestCase):
    def test_tailbone_area(self):
        result = analyze_message("I fell and my ass bones hurt a lot")
        self.assertEqual(result["injury_area"], "tailbone_pelvis")
        self.assertIn("severe_pain_after_injury", result["urgent_flags"])

    def test_knee_area(self):
        self.assertEqual(
            analyze_message("My knee popped")["injury_area"],
            "knee",
        )

    def test_inability_to_walk_is_urgent(self):
        result = analyze_message("I cannot walk because my knee hurts")
        self.assertIn("cannot_bear_weight", result["urgent_flags"])

    def test_fall_from_tree_is_prompt_assessment_flag(self):
        result = analyze_message(
            "I was climbing a tree and fell down and my ass bones hurt a lot"
        )
        self.assertIn("fall_from_height", result["urgent_flags"])
        self.assertIn("severe_pain_after_injury", result["urgent_flags"])

    def test_emergency_breathing(self):
        result = analyze_message("I am having trouble breathing")
        self.assertIn("breathing_or_chest", result["emergency_flags"])

    def test_no_i_cannot_walk_still_means_cannot_walk(self):
        result = analyze_message("No, I cannot walk")
        self.assertIn("cannot_bear_weight", result["urgent_flags"])

    def test_negative_emergency_phrase_is_not_positive(self):
        result = analyze_message("I do not have trouble breathing")
        self.assertNotIn("breathing_or_chest", result["emergency_flags"])

    def test_ambiguous_cant_see(self):
        result = analyze_message("I can't see")
        self.assertTrue(result["ambiguous_vision"])
        self.assertNotIn("sudden_vision_loss", result["emergency_flags"])

    def test_conversation_keeps_earlier_emergency_signal(self):
        messages = [
            {"role": "user", "content": "I fell"},
            {"role": "user", "content": "Now I have trouble breathing"},
            {"role": "assistant", "content": "Call emergency services"},
        ]
        result = analyze_conversation(messages)
        self.assertIn("breathing_or_chest", result["emergency_flags"])


if __name__ == "__main__":
    unittest.main()
