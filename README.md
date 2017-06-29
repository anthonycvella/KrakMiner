# KrakMiner - Vainglory API Parsing Tool

## General Tool Commands
| Argument Name | Short Form    | Long Form | Description                                                                           
|---------------|:-------------:|:---------:|:------------
| Key           | -k            | --key     | Your unique Vainglory Developer API key.
| Region        | -r            | --region  | The region to perform the query on.
| Output        | -o            | --output  | The output directory of the parsed data.
| Verbose       | -v            | --verbose | Enables verbose logging output.

_If you do not have a Vainglory Developer Key, you can signup for one at [http://www.developer.vainglorygame.com](http://www.developer.vainglorygame.com)._

## Supported Query Types
### __Matches__
| Argument Name | Short Form    | Long Form     | Description
|---------------|:-------------:|:-------------:|:-----------
| Offset        | -o            | --offset      | Offset of results, typically used for paging.
| Limit         | -l            | --limit       | The maximum number of results to be returned.
| Player Names  | -pn           | --player-names| The player names to query against.
| Player Ids    | -pi           | --player-ids  | The player ids to query against.
| Team Names    | -tn           | --team-names  | The team names to query against.
| Game Mode     | -gm           | --game-mode   | The game mode to query against.

#### Example
```python
python KrakMiner.py -k [Your API Key] -r na matches -l 50 -pn Snwspeckle
```

_This example is executing a `matches` query against the `na` region, with a limit of `50` and a player name of `Snwspeckle`._