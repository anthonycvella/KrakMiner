import argparse
import csv
import os
from parsers import QueryParsers

# The default output directory
DEFAULT_OUTPUT_DIR      = os.getcwd() + "/Results"
# The supported regions for the API
SUPPORTED_REGIONS       = ['na', 'eu', 'sa', 'ea', 'sg', 'tournament-na', 'tournament-eu', 'tournament-sa', 'tournament-ea', 'tournament-sg']

# Container class for parameters of the general parser
class GeneralParameters(object):
    def __init__(self, key, region, output, verbose):
        self.key        = key
        self.region     = region
        self.output     = output
        self.verbose    = verbose

# Setup function to verify the 'gamelocker' package is installed
def setup():
    # Verify the default output directory exists (./Results), if not create it
    if not os.path.exists(DEFAULT_OUTPUT_DIR):
        os.makedirs(DEFAULT_OUTPUT_DIR)

    try:
        import gamelocker as gamelocker
        return gamelocker
    except ImportError:
        print("Trying to install required module: gamelocker\n")
        os.system('python -m pip install madglory-ezl')

    # Import the supporting library for the Vainglory API
    import gamelocker as gamelocker
    return gamelocker

# Parser function (main program)
def parser():
    # General level parser for generic API parameters
    general_group = argparse.ArgumentParser(add_help=False)
    general_group.add_argument("-k", "--key", required=True, help="Your unique Vainglory Developer API key. If you don't have one, register for one at http://www.developer.vainglorygame.com")
    general_group.add_argument("-r", "--region", choices=SUPPORTED_REGIONS, required=True, help="The region to perform the query on.")
    general_group.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR, help="The output directory of the parsed data.")
    general_group.add_argument("-v", "--verbose", action="store_true", help="Enables verbose logging output.")

    # Top level parser containing the general group & subparsers for the support queries
    top_parser = argparse.ArgumentParser(add_help=False, parents=[general_group])
    subparsers = top_parser.add_subparsers(dest="query")

    # Iterate over each parser to configure it and add it as a subparser
    for item in QueryParsers.getAllParsers():
        # Get the function reference of the parser function
        func = getattr(QueryParsers.Parsers, item)

        # Verify this is a valid function that can be called
        if callable(func):
            # Call the function and return its object
            parser_object = func()

            # Add the parser to our subparsers by the name of the parser
            query_parser = subparsers.add_parser(parser_object.getName())

            # Add the necessary arguments to the parser
            parser_object.arguments(query_parser)

    # Parse the arguments from the arg parser
    args = top_parser.parse_args()

    # Build our general config parameters object
    general_parameters = GeneralParameters(args.key, args.region, args.output, args.verbose)

    # Find the matching function to call based on the query requested
    queries = {"matches": lambda: matches(general_parameters, parser_object.getArguments(args), parser_object)}
    queries[args.query]()

def matches(general_parameters, query_arguments, parser_object):
    # Get our api manager
    api = gamelocker.Vainglory(general_parameters.key)

    # Get the raw data from the API
    data = api.matches(query_arguments, general_parameters.region, toObject=True)

    # Parse the data from the API
    parsed_data = parser_object.parse(data, player_name=query_arguments["filter[playerNames]"], api=api)

    # Write the parsed data to a .csv file
    with open(general_parameters.output + "/KrakMinerDump.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=parser_object.getFieldnames())
        writer.writeheader()
        writer.writerows(parsed_data)

        print("DONE!")

# Main entry function
def main():
    # Run initial setup and set gamelocker to be a global object
    global gamelocker
    gamelocker = setup()

    # Run the parser
    parser()

# Initial main entry function
if __name__ == "__main__":
    main()
