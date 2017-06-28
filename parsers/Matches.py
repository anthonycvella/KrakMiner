import argparse
from parsers.QueryParsers import Query

class Parser(Query):
    def __init__(self, name="matches", endpointUrl="matches"):
        super().__init__(name, endpointUrl)

    def arguments(self, parser):
        parser.add_argument("-o", "--offset", type=int, default=0, help="Offset of results, typically used for paging.")
        parser.add_argument("-l", "--limit", type=int, default=1, help="The maximum number of results to be returned.")
        parser.add_argument("-pn", "--player-names", help="The player names to query against.")
        parser.add_argument("-pi", "--player-ids", help="The player ids to query against.")
        parser.add_argument("-tn", "--team-names", help="The team names to query against.")
        parser.add_argument("-gm", "--game-mode", choices=['casual', 'ranked'], help="The game mode to query against.")

    def parser(self, data):
        pass
