import pickle
from nba_api.stats.endpoints import TeamGameLogs
from nba_api.stats.static import teams

from functions import player_log_df

with open('team_players_dict.pkl', 'rb') as file:
    team_players_dict = pickle.load(file)

# for key, value in team_players_dict.items():
#     for item in value:
#         print(item)

selected_id = '201939'
season = '2023-24'
player_df = player_log_df(selected_id, season)
pts_list = player_df['PTS'].head(15).to_list()
ast_list = player_df['AST'].head(15).to_list()
print(pts_list)
print(ast_list)
