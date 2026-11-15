import unittest
from backend.questions import get_next_question


class TestQuestions(unittest.TestCase):
    def test_tailbone_questions_are_relevant(self):
        question = get_next_question("tailbone_pelvis", set())
        self.assertEqual(question["id"], "leg_weakness")
        self.assertIn("leg", question["question"])

    def test_questions_do_not_repeat(self):
        asked = {"leg_weakness"}
        question = get_next_question("tailbone_pelvis", asked)
        self.assertEqual(question["id"], "leg_numbness")

    def test_returns_none_when_complete(self):
        asked = {
            "leg_weakness",
            "leg_numbness",
            "walking_ability",
            "head_neck_impact",
            "loss_consciousness",
        }
        self.assertIsNone(get_next_question("tailbone_pelvis", asked))


if __name__ == "__main__":
    unittest.main()
