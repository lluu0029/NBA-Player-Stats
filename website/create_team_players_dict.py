import pickle
import time
from website.functions import get_players_in_team
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.static import teams


# nba_teams = teams.get_teams()
# team_dict = {}
# for team in nba_teams:
#     team_dict[team['full_name']] = team['id']


# players_team_dict = {}
# for key, value in team_dict.items():
#     time.sleep(1)
#     players_team_dict[key] = get_players_in_team(value)

# # Saves dictionary of players in a team into team_players_dict.pkl
# with open('website\\team_players_dict.pkl', 'wb') as file:
#     pickle.dump(players_team_dict, file)

# print('Success')