import unittest

class TestVerification(unittest.TestCase):
    def test_safe_refusal_flag(self):
        ambiguous_case = {
            "is_ambiguous": True,
            "refusal_reason": "Blurry dose detected"
        }
        self.assertTrue(ambiguous_case["is_ambiguous"])

if __name__ == "__main__":
    unittest.main()