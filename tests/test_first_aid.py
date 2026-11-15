
import unittest

from backend.first_aid import get_first_aid_guidance


class TestFirstAid(unittest.TestCase):

    def test_soft_tissue_guidance(self):
        result = get_first_aid_guidance("soft_tissue")

        self.assertFalse(result["is_emergency"])
        self.assertIn("instructions", result)
        self.assertGreater(len(result["instructions"]), 0)

    def test_fracture_guidance(self):
        result = get_first_aid_guidance("suspected_fracture")

        self.assertIn(
            "Do not attempt to straighten the limb or put a joint back into place.",
            result["instructions"],
        )

    def test_emergency_overrides_requested_guidance(self):
        result = get_first_aid_guidance(
            "soft_tissue",
            emergency=True,
        )

        self.assertTrue(result["is_emergency"])
        self.assertEqual(result["title"], "Emergency — get help now")

    def test_unknown_category_returns_general_guidance(self):
        result = get_first_aid_guidance("unknown_category")

        self.assertIn("General injury precautions", result["title"])

    def test_guidance_has_version(self):
        result = get_first_aid_guidance("soft_tissue")

        self.assertIn("version", result)
        self.assertIn("status", result)


if __name__ == "__main__":
    unittest.main()
