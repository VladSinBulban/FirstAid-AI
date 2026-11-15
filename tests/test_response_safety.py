import unittest
from backend.response_safety import validate_ai_response


class TestResponseSafety(unittest.TestCase):
    def test_accepts_conservative_summary(self):
        self.assertTrue(
            validate_ai_response(
                "I can't determine the cause from chat. Please tell a trusted adult."
            )[0]
        )

    def test_rejects_medication_advice(self):
        self.assertFalse(
            validate_ai_response("Take ibuprofen and rest.")[0]
        )

    def test_rejects_diagnosis(self):
        self.assertFalse(
            validate_ai_response("You probably have a fracture.")[0]
        )

    def test_rejects_questions(self):
        self.assertFalse(
            validate_ai_response("Can you tell me more?")[0]
        )

    def test_rejects_incomplete_response(self):
        self.assertFalse(
            validate_ai_response("You should avoid")
            [0]
        )


if __name__ == "__main__":
    unittest.main()
