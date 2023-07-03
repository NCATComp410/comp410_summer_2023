import uuid
import spacy
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer, Pattern, RecognizerResult

# make sure en_core_web_lg is loaded correctly
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    from spacy.cli import download

    download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")


def show_aggie_pride():
    """Show Aggie Pride"""
    return 'Aggie Pride - Worldwide'


def generate_uuid():
    """Generate a UUID"""
    return uuid.uuid4()


def analyze_text(text: str, show_supported=False, show_details=False) -> list[str] | list[RecognizerResult]:
    # Overview of Presidio
    # https://microsoft.github.io/presidio/analyzer/

    # Supported entities and adding custom entities
    # https://microsoft.github.io/presidio/supported_entities/
    # https://microsoft.github.io/presidio/analyzer/adding_recognizers/

    # Create an additional pattern to detect a 8-4-4-4-12 UUID
    uuid_pattern = Pattern(name='uuid_pattern',
                           regex=r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b',
                           score=0.9)
    uuid_recognizer = PatternRecognizer(supported_entity='UUID',
                                        patterns=[uuid_pattern])

    banner_id_pattern = Pattern(name='banner_id_pattern',
                                regex=r'\b(\d{9}|\d{6})\b',
                                score=0.9)
    banner_id_recognizer = PatternRecognizer(supported_entity="BANNER_ID",
                                             patterns=[banner_id_pattern])

    # The default SSN detection looks for valid and invalid SSNs. Since we do not want to use
    # a valid SSN for testing purposes, we will create a custom SSN recognizer that will
    # detect a SSN in the format xxx-xx-xxxx and not attempt to validate it further
    # https://github.com/microsoft/presidio/tree/main/presidio-analyzer/presidio_analyzer/predefined_recognizers
    ssn_pattern = Pattern(name='ssn_pattern', regex=r'\b\d{3}-\d{2}-\d{4}\b', score=0.9)
    ssn_recognizer = PatternRecognizer(supported_entity='US_SSN', patterns=[ssn_pattern])

    # Initialize the recognition registry
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers()

    # Add custom recognizers
    registry.add_recognizer(uuid_recognizer)
    registry.add_recognizer(ssn_recognizer)
    registry.add_recognizer(banner_id_recognizer)

    # Set up analyzer with our updated recognizer registry
    analyzer = AnalyzerEngine(registry=registry)

    # Show all entities that can be detected for debugging
    if show_supported:
        return analyzer.get_supported_entities()

    if show_details:
        results = analyzer.analyze(text=text,
                                   language="en",
                                   return_decision_process=show_details)
        print(results)
        for r in results:
            decision_process = r.analysis_explanation
            print(decision_process)
    else:
        results = analyzer.analyze(text=text,
                                   language='en')

    return results


if __name__ == '__main__':
    print(show_aggie_pride())
    print(generate_uuid())
