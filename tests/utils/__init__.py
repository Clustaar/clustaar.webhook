import json
from os import environ, path

from .factory import Factory


FACTORY = Factory()


CURRENT_DIRECTORY = path.dirname(__file__)
RESOURCES_DIRECTORY = path.join(CURRENT_DIRECTORY, "..", "resources")


def resource_path(file_path):
    return path.join(RESOURCES_DIRECTORY, file_path)


def resource_file(file_path):
    full_path = resource_path(file_path)
    return open(full_path, "r")


def resource_content(file_path):
    file = resource_file(file_path)
    content = file.read()
    file.close()
    return content


def load_json_resource(file_path):
    content = resource_content(file_path)
    return json.loads(content)
