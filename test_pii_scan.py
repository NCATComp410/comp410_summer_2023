import unittest
from pii_scan import show_aggie_pride, analyze_text
from typing import List
import pprint
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, EntityRecognizer, Pattern, RecognizerResult
from presidio_analyzer.recognizer_registry import RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine, SpacyNlpEngine, NlpArtifacts
from presidio_analyzer.context_aware_enhancers import LemmaContextAwareEnhancer

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

        results = analyze_text('thisisanemail@gmail.com')
        self.assertNotIn('PHONE_NUMBER', str(results))

    def test_zipcode(self):
        regex = r"(\b\d{5}(?:\-\d{4})?\b)"
        zipcode_pattern = Pattern(name="zip code (weak)", regex=regex, score=0.01)

# Define the recognizer with the defined pattern
        zipcode_recognizer = PatternRecognizer(supported_entity="US_ZIP_CODE", patterns = [zipcode_pattern])

        registry = RecognizerRegistry()
        registry.add_recognizer(zipcode_recognizer)
        analyzer = AnalyzerEngine(registry=registry)


#Positive Test zipcode
        results = analyzer.analyze(text="My zip code is 90010",language="en")
        print(results)
        self.assertRegex(r"(\b\d{5}\b)",str(results))
        
        results = analyzer.analyze(text="My zip code is 12519",language="en")
        print(results)
        self.assertRegex(r"(\b\d{5}\b)",str(results))
#Negative test code: Comment out section to see the differnce
        # results = analyzer.analyze(text="My zip code is 1234",language="en")
        # print(results)
        # self.assertRegex(r"(\b\d{5}\b)",str(results))


if __name__ == '__main__':
    unittest.main()
