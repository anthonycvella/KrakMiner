import argparse
import csv
import os
from parsers import QueryParsers

# Setup function to verify the 'gamelocker' package is installed
def setup():
    try:
        import gamelocker as gamelocker
        return gamelocker
    except ImportError:
        print("Trying to install required module: gamelocker\n")
        os.system('python -m pip install madglory-ezl')

    # Import the supporting library for the VGAPI
    import gamelocker

# Container class for parameters of the general parser
class GeneralParameters(object):
    def __init__(self, key, region, output, verbose):
        self.key        = key
        self.region     = region
        self.output     = output
        self.verbose    = verbose

# Parser function (main program)
def parser(gamelocker):
    # The supported regions the API can reach
    region_choices = ['na', 'eu', 'sa', 'ea', 'sg', 'tournament-na', 'tournament-eu', 'tournament-sa', 'tournament-ea', 'tournament-sg']

    # General level parser for generic API parameters
    general_group = argparse.ArgumentParser(add_help=False)
    general_group.add_argument("-k", "--key", required=True, help="Your unique Vainglory Developer API key. If you don't have one, register for one at http://www.developer.vainglorygame.com")
    general_group.add_argument("-r", "--region", choices=region_choices, required=True, help="The region to perform the query on.")
    general_group.add_argument("-o", "--output", default=os.getcwd() + "/Results", help="The output directory of the parsed data.")
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

    def matches(general_parameters, player_name):
        api = gamelocker.Vainglory(general_parameters.key)
        args = {'page[limit]': '1', 'filter[playerNames]': player_name, 'sort': '-createdAt'}
        data = api.matches(args, general_parameters.region, toObject=True)

        with open(general_parameters.output + "/KrakMinerDump.csv", "w", newline="") as csvfile:
            # Column names for the spreadsheet
            fieldnames = ['match_id', 'player_id', 'player_name', 'actor', 'is_winner', 'ban_team_1', 'ban_team_2', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_6']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for match in data:
                print("Parsing Match ID: " + match.id)
                participant_obj = None

                # Get the players participant object
                for roster in match.rosters:
                    for participant in roster["participants"]:
                        if participant["player"]["name"] == player_name:
                            participant_obj = participant

                # Create empty items list array
                items_list = ["", "", "", "", "", "", ""]

                # Build the items array from the participant
                if participant_obj != None:
                    for i in range(len(participant_obj["items"])):
                        try:
                            items_list[i] = (participant_obj["items"][i])
                        except IndexError:
                            pass

                # Get our bans from telemetry
                ban_team_1 = ""
                ban_team_2 = ""
                telemetry_data = api.telemetry(match.telemetry.URL)
                for telemetry in telemetry_data:
                    if telemetry["type"] == "HeroBan":
                        if telemetry["payload"]["Team"]:
                            if telemetry["payload"]["Team"] == "1":
                                ban_team_1 = telemetry["payload"]["Hero"]
                            elif telemetry["payload"]["Team"] == "2":
                                ban_team_2 = telemetry["payload"]["Hero"]
                    if ban_team_1 != "" and ban_team_2 != "":
                        break

                # Write our rows
                writer.writerow({'match_id': match.id,
                                 'player_id': participant_obj["player"]["id"],
                                 'player_name': participant_obj["player"]["name"],
                                 'actor': participant_obj["actor"],
                                 'is_winner': participant_obj["winner"],
                                 'ban_team_1': ban_team_1,
                                 'ban_team_2': ban_team_2,
                                 'item_1': items_list[0],
                                 'item_2': items_list[1],
                                 'item_3': items_list[2],
                                 'item_4': items_list[3],
                                 'item_5': items_list[4],
                                 'item_6': items_list[5]})

        print("DONE!")

    # Build our general config parameters object
    general_parameters = GeneralParameters(args.key, args.region, args.output, args.verbose)

    # Find the matching function to call based on the query requested
    queries = {"matches": lambda: matches(general_parameters, args.player_names)}
    queries[args.query]()

# Main entry function
def main():
    # Run initial setup
    gamelocker = setup()

    # Run the parser
    parser(gamelocker)

# Initial main entry function
if __name__ == "__main__":
    main()
