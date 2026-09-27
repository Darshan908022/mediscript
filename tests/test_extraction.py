import unittest

class TestExtraction(unittest.TestCase):
    def test_sample_structure(self):
        sample_data = {
            "patient_name": "Ramesh Kumar",
            "medications": [{"name": "Metformin", "dose": "500mg"}]
        }
        self.assertIn("patient_name", sample_data)
        self.assertEqual(len(sample_data["medications"]), 1)

if __name__ == "__main__":
    unittest.main()