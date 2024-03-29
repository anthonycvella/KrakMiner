import argparse

# Helper function to get all the supported query parsers
def getAllParsers():
    return [func for func in dir(Parsers) if callable(getattr(Parsers, func)) and not func.startswith("__")]

# Base class of which all query parses derive from
class Query(object):
    def __init__(self, name, endpointUrl, fieldnames):
        self.name           = name
        self.endpointUrl    = endpointUrl
        self.fieldnames     = fieldnames

    def getName(self):
        return self.name

    def getEndpointUrl(self):
        return self.endpointUrl

    def getFieldnames(self):
        return self.fieldnames

    def arguments(self, parser):
        pass

    def getArguments(self, args):
        pass

    def parse(self, data):
        pass

# Defines all of the supported parsers
class Parsers(object):

    @staticmethod
    def matches():
        from parsers.Matches import Parser
        return Parser()
