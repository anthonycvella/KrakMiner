import argparse
from parsers.QueryParsers import Query

# The headers name for the output .CSV file
FIELDNAMES = ['match_id', 'player_id', 'player_name', 'actor', 'is_winner', 'ban_team_1', 'ban_team_2', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_6']

class Parser(Query):
    def __init__(self, name="matches", endpointUrl="matches"):
        super().__init__(name, endpointUrl, FIELDNAMES)

    def arguments(self, parser):
        parser.add_argument("-o", "--offset", type=int, default=0, help="Offset of results, typically used for paging.")
        parser.add_argument("-l", "--limit", type=int, default=1, help="The maximum number of results to be returned.")
        parser.add_argument("-pn", "--player-names", help="The player names to query against.")
        parser.add_argument("-pi", "--player-ids", help="The player ids to query against.")
        parser.add_argument("-tn", "--team-names", help="The team names to query against.")
        parser.add_argument("-gm", "--game-mode", choices=['casual', 'ranked'], help="The game mode to query against.")

    def getArguments(self, args):
        return {"page[offset]": args.offset,
                "page[limit]": args.limit,
                "filter[playerNames]": args.player_names,
                "filter[playerIds": args.player_ids,
                "filter[teamNames]": args.team_names,
                "filter[gameMode]": args.game_mode}

    def parse(self, data, **parameters):
        # Get the optional player_name parameter
        if "player_name" in parameters:
            player_name = parameters["player_name"]

        # Get the optional api object in parameter
        if "api" in parameters:
            api = parameters["api"]

        # The container list of all matches for the dataset
        matches_list = []

        # Iterate over each match in the data
        for match in data:
            # The match dictionary where each data point is added to
            match_dict = {}

            print("Parsing Match ID: " + match.id)

            # Add match id to the match dictionary (FIELDNAMES INDEX: 0)
            match_dict.update({FIELDNAMES[0]: match.id})

            # Get the participant object for our player
            participant_obj = self.getParticipant(match, player_name)

            # Add players id to the match dictionary (FIELDNAMES INDEX: 1)
            match_dict.update({FIELDNAMES[1]: participant_obj["player"]["id"]})

            # Add players name to the match dictionary (FIELDNAMES INDEX: 2)
            match_dict.update({FIELDNAMES[2]: participant_obj["player"]["name"]})

            # Add players actor to the match dictionary (FIELDNAMES INDEX: 3)
            match_dict.update({FIELDNAMES[3]: participant_obj["actor"]})

            # Add is winner to the match dictionary (FIELDNAMES INDEX: 4)
            match_dict.update({FIELDNAMES[4]: participant_obj["winner"]})

            # Get a dictionary of the bans
            bans_dict = self.getBans(api, match.telemetry.URL)

            # Add ban team 1 to the match dictionary (FIELDNAMES INDEX: 5)
            match_dict.update({FIELDNAMES[5]: bans_dict["team_1"]})

            # Add ban team 2 to the match dictionary (FIELDNAMES INDEX: 6)
            match_dict.update({FIELDNAMES[6]: bans_dict["team_2"]})

            # Get all items from the participant
            items = self.getItems(participant_obj["items"])

            # Add items to the match dictionary (FIELDNAMES INDEX: 7...X)
            for i, item in enumerate(items):
                try:
                    match_dict.update({FIELDNAMES[i + 7]: item})
                except IndexError:
                    pass

            # Append the match dictionary to the list of all matches
            matches_list.append(match_dict)

        return matches_list

    # Gets the participant object from a match based on the player name
    def getParticipant(self, match, player_name):
        for roster in match.rosters:
            for participant in roster["participants"]:
                if participant["player"]["name"] == player_name:
                    return participant

    # Gets the bans of a match
    def getBans(self, api, telemetryUrl):
        bans = {}
        telemetry_data = api.telemetry(telemetryUrl)
        for telemetry in telemetry_data:
            if telemetry["type"] == "HeroBan":
                if telemetry["payload"]["Team"]:
                    if telemetry["payload"]["Team"] == "1":
                        bans.update({"team_1": telemetry["payload"]["Hero"]})
                    elif telemetry["payload"]["Team"] == "2":
                        bans.update({"team_2": telemetry["payload"]["Hero"]})
            if "team_1" in bans and "team_2" in bans:
                break

        if "team_1" not in bans:
            bans.update({"team_1": None})

        if "team_2" not in bans:
            bans.update({"team_2": None})

        return bans

    # Gets all items from a match
    def getItems(self, items):
        # Create empty items list of 6 items (Max amount of items)
        items_list = ["", "", "", "", "", ""]

        # Build the items array from the participant
        if items != None:
            for i, item in enumerate(items):
                try:
                    items_list[i] = item
                except IndexError:
                    pass

        return items_list
