import unittest
from pii_scan import show_aggie_pride, analyze_text
from presidio_analyzer import RecognizerResult


class TestPIIScan(unittest.TestCase):
    def test_aggie_pride(self):
        self.assertEqual('Aggie Pride - Worldwide', show_aggie_pride())

    def test_show_supported_entities(self):
        # test the show_supported_entities function
        # https://microsoft.github.io/presidio/supported_entities/
        results = analyze_text('This is a test', show_supported=True)
        print(results)
        self.assertTrue(True)

    def test_uuid(self):
        # test a valid UUID for detection
        results = analyze_text('This is a UUID: 123e4567-e89b-12d3-a456-42665234000c')
        self.assertIn('UUID', str(results))

        # test some uppercase letters
        results = analyze_text('This is a UUID: 123E4567-e89B-12d3-a456-4266523400FF')
        self.assertIn('UUID', str(results))

        # test an invalid UUID for detection
        results = analyze_text('This is not a UUID: 123e4567-e89b-12d3-a456-42665234000')
        self.assertNotIn('UUID', str(results))

    def test_political_group_detection(self):
        # test a valid political group
        results = analyze_text('I am a Democrat')
        self.assertIn('NRP', str(results))

        results = analyze_text('I am a Republican')
        self.assertIn('NRP', str(results))

        results = analyze_text('This is a democracy')
        self.assertNotIn('NRP', str(results))

    def test_IPv4_address_detection(self):
        # test for a valid IPv4 address. (no alphabet or special characters)
        results = analyze_text('123.123.123.123')
        print(results)
        self.assertIn('IP_ADDRESS', str(results))

        results = analyze_text('!&^*.R#S.123.TY$')
        self.assertNotIn('NRP', str(results))

        results = analyze_text('DAa.ReS.unj.TYn')
        self.assertNotIn('NRP', str(results))

        results = analyze_text('1234.1243.1235.1235')
        self.assertNotIn('NRP', str(results))





if __name__ == '__main__':
    unittest.main()
