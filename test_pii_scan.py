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

    def test_phone_number_detection(self):
        # test a valid phone number
        results = analyze_text('9992224444')
        self.assertIn('PHONE_NUMBER', str(results))

        results = analyze_text('999-222-4444')
        self.assertIn('PHONE_NUMBER', str(results))

        results = analyze_text('999.222.4444')
        self.assertIn('PHONE_NUMBER', str(results))

        results = analyze_text('(999)222-4444')
        self.assertIn('PHONE_NUMBER', str(results))
  
        results = analyze_text('1-999-222-4444')
        self.assertIn('PHONE_NUMBER', str(results))

        #results = analyze_text('+1(999)222-444')
        #self.assertIn('PHONE_NUMBER', str(results))

        results = analyze_text('999-22-4444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999224444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999.22.4444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999224444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999-222-444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('(999)222-444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999.222.444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999-222-444444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999222444444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('999.222.444444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        results = analyze_text('(999)222-444444')
        self.assertNotIn('PHONE_NUMBER', str(results))

        esults = analyze_text('thisisanemail@gmail.com')
        self.assertNotIn('PHONE_NUMBER', str(results))

    def test_social_security_detection(self):
            # test a valid social secutiy number 
        results = analyze_text('This is a SSN: 111-00-1111')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 222-00-2222')
        self.assertIn('US_SSN' , str(results))

        results = analyze_text('This is a SSN: 000-11-0000')
        self.assertIn('US_SSN' , str(results))

        results = analyze_text('This is a SSN: 555-00-5555')
        self.assertIn('US_SSN' , str(results))
        
        results = analyze_text('This is a SSN: 666-00-6666')
        self.assertIn('US_SSN' , str(results))

        results = analyze_text('This is a SSN: 777-00-7777')
        self.assertIn('US_SSN' , str(results))

        results = analyze_text('This is a SSN: 666-11-6666')
        self.assertIn('US_SSN' , str(results))

        results = analyze_text('This is a SSN: 000-11-1000')
        self.assertIn('US_SSN' , str(results))

        results = analyze_text('This is not a SSN: 947-603-4211')
        self.assertNotIn('US_SSN' , str(results))

        results = analyze_text('This is not a SSN: 1256547632')
        self.assertNotIn('US_SSN' , str(results))

        results = analyze_text('This is not a SSN: 000,46,8789')
        self.assertNotIn('US_SSN' , str(results))

        results = analyze_text('This is not a SSN: #ABCDEFAB')
        self.assertNotIn('US_SSN' , str(results))

        results = analyze_text('This is not a SSN: +1233456689')
        self.assertNotIn('US_SSN' , str(results))

        
if __name__ == '__main__':
    unittest.main()
