import unittest
from pii_scan import show_aggie_pride


class TestPIIScan(unittest.TestCase):
    def test_aggie_pride(self):
        self.assertEqual('Aggie Pride - Worldwide', show_aggie_pride())
    def test_email_detection(self):
        # Test a valid email input
        results = analyze_text('user@gmail.com')
        self.assertIn('EMAIL', str(results))

        results = analyze_text('33nature@aol.com')
        self.assertIn('EMAIL', str(results))

        results = analyze_text('__2002@www.google.com')
        self.assertNotIn('EMAIL', str(results))

        results = analyze_text('user_2@apple.com')
        self.assertIn('EMAIL', str(results))

        results = analyze_text('aggie+pride@aggies.ncat.edu')
        self.assertNotIn('EMAIL', str(results))


if __name__ == '__main__':
    unittest.main()
