import unittest
from pii_scan import show_aggie_pride, analyze_text, anonymize_text


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

    def test_zipcode(self):
        results = analyze_text('11011')
        self.assertIn('ZIP_CODE', str(results))

        results = analyze_text('Zipcode: 11011')
        self.assertIn('ZIP_CODE', str(results))

        results = analyze_text('20011')
        self.assertIn('ZIP_CODE', str(results))

        results = analyze_text('10011-0012')
        self.assertIn('ZIP_CODE', str(results))

        results = analyze_text('110011')
        self.assertNotIn('ZIP_CODE', str(results))

        results = analyze_text('1100')
        self.assertNotIn('ZIP_CODE', str(results))

        results = analyze_text('11001-221')
        self.assertNotIn('ZIP_CODE', str(results))

    def test_political_group_detection(self):
        # test a valid political group
        results = analyze_text('I am a Democrat')
        self.assertIn('NRP', str(results))

        results = analyze_text('I am a Republican')
        self.assertIn('NRP', str(results))

        results = analyze_text('This is a democracy')
        self.assertNotIn('NRP', str(results))

    def test_date_of_birth_detection(self):
        # test a valid date of birth detection
        results = analyze_text('12/23/2001')
        print(results)
        self.assertIn('DATE_TIME', str(results))
        
        # test a invalid date of birth detection
        results = analyze_text('bc/!-34/iuo')
        self.assertNotIn('DATE_TIME', str(results))

        results = analyze_text('12-234-2034')
        self.assertNotIn('DATE_TIME', str(results))

    def test_name_detection(self):
        # test a valid name
        results = analyze_text('Jason Bond')
        self.assertIn('PERSON', str(results))

        results = analyze_text('Primrose R. Everdean')
        self.assertIn('PERSON', str(results))

        results = analyze_text('Tony Robbins is my favorite salesman.')
        self.assertIn('PERSON', str(results))

        results = analyze_text('Jada Pinkett-Smith')
        self.assertIn('PERSON', str(results))

        results = analyze_text('This is a regular sentence.')
        self.assertNotIn('PERSON', str(results))

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

        # results = analyze_text('+1(999)222-444')
        # self.assertIn('PHONE_NUMBER', str(results))

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

        results = analyze_text('thisisanemail@gmail.com')
        self.assertNotIn('PHONE_NUMBER', str(results))
        
    def test_IPv4_address_detection(self):
        # test for a valid IPv4 address. (no alphabet or special characters)
        results = analyze_text('123.123.123.123')
        print(results)
        self.assertIn('IP_ADDRESS', str(results))

        results = analyze_text('!&^*.R#S.123.TY$')
        self.assertNotIn('IP_ADDRESS', str(results))

        results = analyze_text('DAa.ReS.unj.TYn')
        self.assertNotIn('IP_ADDRESS', str(results))

        results = analyze_text('1234.1243.1235.1235')
        self.assertNotIn('IP_ADDRESS', str(results))

    def test_religous_affiliation_detection(self):
        # Positive Test for valid relgious group
        results = analyze_text('I am a Christian')
        self.assertIn('NRP', str(results))

        results = analyze_text('I am a Muslim')
        self.assertIn('NRP', str(results))

        results = analyze_text('I am a Buddhist')
        self.assertIn('NRP', str(results))

        # Negative Test Case
        results = analyze_text('He is Religious')
        self.assertNotIn('NRP', str(results))

    def test_social_security_detection(self):
        # test a valid social secutiy number
        results = analyze_text('This is a SSN: 111-00-1111')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 222-00-2222')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 000-11-0000')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 555-00-5555')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 666-00-6666')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 777-00-7777')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 666-11-6666')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is a SSN: 000-11-1000')
        self.assertIn('US_SSN', str(results))

        results = analyze_text('This is not a SSN: 947-603-4211')
        self.assertNotIn('US_SSN', str(results))

        results = analyze_text('This is not a SSN: 1256547632')
        self.assertNotIn('US_SSN', str(results))

        results = analyze_text('This is not a SSN: 000,46,8789')
        self.assertNotIn('US_SSN', str(results))

        results = analyze_text('This is not a SSN: #ABCDEFAB')
        self.assertNotIn('US_SSN', str(results))

        results = analyze_text('This is not a SSN: +1233456689')
        self.assertNotIn('US_SSN', str(results))

    def test_banner_id_detection(self):
        # test a valid banner id
        results = analyze_text("950754556")
        self.assertIn('BANNER_ID', str(results))

        results = analyze_text("987867")
        self.assertIn('BANNER_ID', str(results))

        results = analyze_text("098bbjk923")
        self.assertNotIn('BANNER_ID', str(results))

        results = analyze_text("09923")
        self.assertNotIn('BANNER_ID', str(results))

    def test_cc_number_detection(self):
        # test a (possibly) valid credit card number
        # https://developer.squareup.com/docs/devtools/sandbox/payments
        cc_nums = {'Visa': '4111 1111 1111 1111',
                   'Mastercard': '5105 1051 0510 5100',
                   'Discover': '6011 0000 0000 0004',
                   'Diners Club': '3000 000000 0004',
                   'JCB': '3566 1111 1111 1113',
                   'American Express': '3400 000000 00009'}

        for cc_type, cc_num in cc_nums.items():
            print('testing {} number: {}'.format(cc_type, cc_num))
            results = analyze_text(cc_num)
            print(results)
            self.assertIn('CREDIT_CARD', str(results))

        # test an invalid credit card number
        results = analyze_text('1234 5678 9012 3456')
        self.assertNotIn('CREDIT_CARD', str(results))

    def test_anonymizer(self):
        """Implement a quick test on the anonymizer"""
        # positive phone number test
        anon = anonymize_text('This is a phone number test +1-919-555-1212')
        self.assertEqual(anon.text, 'This is a phone number test <PHONE_NUMBER>')

        # negative phone number test
        anon = anonymize_text('This is not a phone number test 55-1212')
        # nothing should be anonymized
        self.assertEqual(anon.text, 'This is not a phone number test 55-1212')


    def test_US_DRIVER_LICENSE(self):
        #test a valid US Drivers License
        results = analyze_text('005644532728')
        print(results)
        self.assertIn('US_DRIVER_LICENSE', str(results))

        results = analyze_text('1111*2222-3333/4444')
        self.assertNotIn('US_DRIVER_LICENSE', str(results))

        results = analyze_text('123/456+789*11222')
        self.assertNotIn('US_DRIVER_LICENSE', str(results))
                        


if __name__ == '__main__':
    unittest.main()
