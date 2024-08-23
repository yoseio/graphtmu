from os import environ, path

DATA_PATH = path.normpath(path.join(path.dirname(__file__), "../../../data"))

NEO4J_URI = environ["NEO4J_URI"]
NEO4J_DATABASE = environ["NEO4J_DATABASE"]
NEO4J_USER = environ["NEO4J_USER"]
NEO4J_PASSWORD = environ["NEO4J_PASSWORD"]
