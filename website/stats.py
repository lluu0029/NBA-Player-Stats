from nba_api.stats.static import players
from website.functions import player_log_df, odds_calc
from statistics import mean

nba_players = players.get_players()

# for player in nba_players:
#     if 'Stephen' in player['full_name'] and 'Curry' in player['full_name']:
#         print(player['id'])

# Steph Curry id
player_id = '201939'
player_team = 'GSW'

player_df = player_log_df(player_id, '2022-23')
print(player_df.to_string())
print(player_df['PTS'].head(5))

for value in player_df['PTS'].head(5):
    if value > 30:
        print(True)
    else:
        print(False)

lst_player = player_df['PTS'].head(9).to_list()
print(lst_player)
print(odds_calc(lst_player, 25))