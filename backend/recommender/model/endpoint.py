class Endpoint:
    endpoint: str
    description: str
    bow: list[str]

    def __init__(self, endpoint: str, description: str, bow: list[str]):
        self.endpoint = endpoint
        self.description = description
        self.bow = bow