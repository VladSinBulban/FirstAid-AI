
import unittest

from backend.chat_safety import parse_emergency_confirmation


class TestChatSafety(unittest.TestCase):

    def test_clear_yes(self):
        self.assertTrue(parse_emergency_confirmation("yes"))

    def test_clear_no(self):
        self.assertFalse(parse_emergency_confirmation("no"))

    def test_yes_with_explanation(self):
        self.assertTrue(
            parse_emergency_confirmation("yes, I am")
        )

    def test_no_with_explanation(self):
        self.assertFalse(
            parse_emergency_confirmation("no, I don't")
        )

    def test_unclear_answer(self):
        self.assertIsNone(
            parse_emergency_confirmation("maybe")
        )

    def test_empty_answer(self):
        self.assertIsNone(
            parse_emergency_confirmation("")
        )


if __name__ == "__main__":
    unittest.main()
