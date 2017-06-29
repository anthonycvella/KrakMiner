# KrakMiner - Vainglory API Parsing Tool



# General Tool Commands
| Argument Name | Short Form    | Long Form | Description |
|---------------|:-------------:|:---------:|:------------|
| Key           | -k            | --key     | Your unique Vainglory Developer API key. If you don't have one, register for one at http://www.developer.vainglorygame.com |
| Region        | -r            | --region  | The region to perform the query on. |
| Output        | -o            | --output  | The output directory of the parsed data. |
| Verbose       | -v            | --verbose | Enables verbose logging output. |

# Supported Query Types
## __Matches__
| Argument Name | Short Form    | Long Form     | Description                                   |
|---------------|:-------------:|:-------------:|:----------------------------------------------|
| Offset        | -o            | --offset      | Offset of results, typically used for paging. |
| Limit         | -l            | --limit       | The maximum number of results to be returned. |
| Player Names  | -pn           | --player-names| The player names to query against.            |
| Player Ids    | -pi           | --player-ids  | The player ids to query against.              |
| Team Names    | -tn           | --team-names  | The team names to query against.              |
| Game Mode     | -gm           | --game-mode   | The game mode to query against.               |

### Example
`python KrakMiner.py -k $YOUR_API_KEY$ -r na -l 50 -pn Snwspeckle`