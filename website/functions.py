import numpy as np
import pandas as pd
from nba_api.stats.endpoints import TeamGameLogs, PlayerGameLogs, BoxScoreAdvancedV2, commonallplayers


# Dataframe of a teams game logs in a season.
def create_team_log_df(team_id, season):
    team_logs_dict = TeamGameLogs(team_id_nullable=team_id, season_nullable=season).get_dict()
    results_dict = team_logs_dict['resultSets']
    headers = results_dict[0]['headers']
    team_logs = results_dict[0]['rowSet']

    df = pd.DataFrame(team_logs, columns=headers)
    return df


# Dataframe of all player game logs.
def player_log_df(player_id, season):
    gamelogs_dict = PlayerGameLogs(player_id_nullable=player_id, season_nullable=season).get_normalized_dict()
    gamelogs = gamelogs_dict['PlayerGameLogs']
    gamelogs_arr = {}
    for item in gamelogs:
        for key, value in item.items():
            if key not in gamelogs_arr.keys():
                gamelogs_arr[key] = np.array(value)
            else:
                array = gamelogs_arr[key]
                new_array = np.append(array, np.array(value))
                gamelogs_arr[key] = new_array
    player_df = pd.DataFrame(gamelogs_arr)


    return player_df


# Dataframe of opponent teams faced by the player containing advanced stats.
def opp_team_adv_stats_df(player_df, player_team):
    boxscore_df = pd.DataFrame()

    for game_id in player_df['GAME_ID']:
        boxscore = BoxScoreAdvancedV2(game_id=game_id).team_stats.get_dict()
        team_data = boxscore['data']

        boxscore_df = boxscore_df._append(team_data, ignore_index=True)

    boxscore_df.columns = ['GAME_ID', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'MIN',
                               'E_OFF_RATING', 'OFF_RATING', 'E_DEF_RATING', 'DEF_RATING', 'E_NET_RATING', 'NET_RATING',
                               'AST_PCT', 'AST_TOV', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'E_TM_TOV_PCT',
                               'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 'E_USG_PCT', 'E_PACE', 'PACE',
                               'PACE_PER40', 'POSS', 'PIE']
    # Filter out games containing the player's team.
    filter = boxscore_df['TEAM_ABBREVIATION'] != player_team
    filtered_df = boxscore_df[filter]

    return filtered_df


def odds_calc(lst, int_over):
    num_items = len(lst)

    counter = 0
    for item in lst:
        if item >= int_over:
            counter += 1

    return [round(1/(counter/num_items), 2), str((round(counter/num_items*100, 2))) + '%']


# Returns a list of dictionaries for each player with their id and name.
def get_players_in_team(team_id):
    # Make the API request to get all players
    players_endpoint = commonallplayers.CommonAllPlayers()
    players_data = players_endpoint.get_data_frames()[0]

    # Filter players based on the specified team_id
    players_in_team = players_data[players_data['TEAM_ID'] == team_id]

    # Extract relevant player information
    player_list = players_in_team[['PERSON_ID', 'DISPLAY_FIRST_LAST']].to_dict(orient='records')

    return player_list