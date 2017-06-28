import argparse

# Helper function to get all the supported query parsers
def getParsers():
    return [func for func in dir(Parsers) if callable(getattr(Parsers, func)) and not func.startswith("__")]

# Base class of which all query parses derive from
class Query(object):

    def __init__(self, name, endpointUrl):
        self.name           = name
        self.endpointUrl    = endpointUrl

    def getName(self):
        return self.name

    def getEndpointUrl(self):
        return self.endpointUrl

    def arguments(self, parser):
        pass

# Defines all of the supported parsers
class Parsers(object):

    @staticmethod
    def matches():
        return Matches()

class Matches(Query):
    def __init__(self, name="matches", endpointUrl="matches"):
        super().__init__(name, endpointUrl)

    def arguments(self, parser):
        parser.add_argument("-o", "--offset", type=int, default=0, help="Offset of results, typically used for paging.")
        parser.add_argument("-l", "--limit", type=int, default=1, help="The maximum number of results to be returned.")
        parser.add_argument("-pn", "--player-names", help="The player names to query against.")
        parser.add_argument("-pi", "--player-ids", help="The player ids to query against.")
        parser.add_argument("-tn", "--team-names", help="The team names to query against.")
        parser.add_argument("-gm", "--game-mode", choices=['casual', 'ranked'], help="The game mode to query against.")