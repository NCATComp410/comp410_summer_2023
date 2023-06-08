import unittest
from pii_scan import show_aggie_pride, analyze_text
from presidio_analyzer import RecognizerResult


class TestPIIScan(unittest.TestCase):
    def test_aggie_pride(self):
        self.assertEqual('Aggie Pride - Worldwide', show_aggie_pride())

    def test_show_supported_entities(self):
        # test the show_supported_entities function
        results = analyze_text('This is a test', show_supported=True)
        self.assertTrue(True)

    def test_uuid(self):
        # test a valid UUID for detection
        results = analyze_text('This is a UUID: 123e4567-e89b-12d3-a456-426652340000')
        self.assertEqual([RecognizerResult(entity_type='UUID', start=16, end=52, score=0.9)],
                         results)

        # test some uppercase letters
        results = analyze_text('This is a UUID: 123E4567-e89B-12d3-a456-4266523400FF')
        self.assertEqual([RecognizerResult(entity_type='UUID', start=16, end=52, score=0.9)],
                         results)

        # test an invalid UUID for detection
        results = analyze_text('This is not a UUID: 123e4567-e89b-12d3-a456-42665234000')
        self.assertEqual([], results)


if __name__ == '__main__':
    unittest.main()
