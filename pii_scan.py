import uuid


def show_aggie_pride():
    """Show Aggie Pride"""
    return 'Aggie Pride - Worldwide'


def generate_uuid():
    """Generate a UUID"""
    return uuid.uuid4()


if __name__ == '__main__':
    print(show_aggie_pride())
    print(generate_uuid())
