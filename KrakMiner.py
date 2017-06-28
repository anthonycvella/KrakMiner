import argparse
import csv
import os
import QueryParsers

try:
    import gamelocker
except ImportError:
    print ("Trying to install required module: gamelocker\n")
    os.system('python -m pip install madglory-ezl')

# Import the supporting library for the VGAPI
import gamelocker

# The supported regions the API can reach
regionChoices = ['na', 'eu', 'sa', 'ea', 'sg', 'tournament-na', 'tournament-eu', 'tournament-sa', 'tournament-ea', 'tournament-sg']

# API level parser for generic API required parameters
api_group = argparse.ArgumentParser(add_help=False)
api_group.add_argument("-k", "--key", required=True, help="Your unique Vainglory Developer API key. If you don't have one, register for one at http://www.developer.vainglorygame.com")
api_group.add_argument("-r", "--region", choices=regionChoices, required=True, help="The region you'd like to perform the query on.")
api_group.add_argument("-o", "--output", default=os.getcwd() + "/Results", help="The output directory of the parsed data.")
api_group.add_argument("-v", "--verbose", action="store_true", help="Enables verbose logging output.")

# Top level parser containg the api group & subparsers for the support queries
parser = argparse.ArgumentParser(add_help=False, parents=[api_group])
subparsers = parser.add_subparsers(dest="query")

# Iterate over each parser to configure it and add it as a subparser
for item in QueryParsers.getParsers():
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
args = parser.parse_args()

def matches(player_name, api_key):
    api = gamelocker.Vainglory(api_key)
    args = {'page[limit]': '1', 'filter[playerNames]': player_name, 'sort': '-createdAt'}
    data = api.matches(args, toObject=True)

    # Get the home directory path
    homePath = os.path.join(os.environ["HOMEPATH"], "Desktop")

    with open(homePath + "/KrakMinerDump.csv", "w", newline="") as csvfile:
        # Column names for the spreadsheet
        fieldnames = ['match_id', 'player_id', 'player_name', 'actor', 'is_winner', 'ban_team_1', 'ban_team_2', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_6']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for match in data:
            print ("Parsing Match ID: " + match.id)
            participantObj = None

            # Get the players participant object
            for roster in match.rosters:
                for participant in roster["participants"]:
                    if participant["player"]["name"] == player_name:
                        participantObj = participant

            # Create empty items list array
            itemsList = ["", "", "", "", "", "", ""]

            # Build the items array from the participant
            if participantObj != None:
                for i in range(len(participantObj["items"])):
                    try:
                        itemsList[i] = (participantObj["items"][i])
                    except IndexError:
                        pass

            # Get our bans from telemetry
            banTeam1 = ""
            banTeam2 = ""
            telemetryData = api.telemetry(match.telemetry.URL)
            for telemetry in telemetryData:
                if telemetry["type"] == "HeroBan":
                    if telemetry["payload"]["Team"]:
                        if telemetry["payload"]["Team"] == "1":
                            banTeam1 = telemetry["payload"]["Hero"]
                        elif telemetry["payload"]["Team"] == "2":
                            banTeam2 = telemetry["payload"]["Hero"]
                if banTeam1 != "" and banTeam2 != "":
                    break

            # Write our rows
            writer.writerow({'match_id': match.id,
                            'player_id': participantObj["player"]["id"],
                            'player_name': participantObj["player"]["name"],
                            'actor': participantObj["actor"],
                            'is_winner': participantObj["winner"],
                            'ban_team_1': banTeam1,
                            'ban_team_2': banTeam2,
                            'item_1': itemsList[0],
                            'item_2': itemsList[1],
                            'item_3': itemsList[2],
                            'item_4': itemsList[3],
                            'item_5': itemsList[4],
                            'item_6': itemsList[5]})

    print ("DONE!")

# Find the matching function to call based on the query requested
queries = {"matches": lambda: matches(args.player_names, args.key)}
queries[args.query]()
