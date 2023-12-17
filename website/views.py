import os
import pickle

from flask import Blueprint, render_template, request, redirect, jsonify
from website.functions import player_log_df, odds_calc
from nba_api.stats.static import teams
from website.create_team_players_dict import get_players_in_team

views = Blueprint('views', __name__)

player_id = '201939'
season = '2023-24'

nba_teams = teams.get_teams()
team_dict = {}
for team in nba_teams:
    team_dict[team['abbreviation']] = team['id']





@views.route('/', methods=['GET', 'POST'])
def main_stats():
    file_path = os.path.join(os.path.dirname(__file__), 'team_players_dict.pkl')
    with open(file_path, 'rb') as file:
        team_players_dict = pickle.load(file)
    return render_template('graph.html', team_dict=team_dict, team_players_dict=team_players_dict)


@views.route('/menu')
def menu():
    file_path = os.path.join(os.path.dirname(__file__), 'team_players_dict.pkl')
    with open(file_path, 'rb') as file:
        team_players_dict = pickle.load(file)

    return render_template('teams.html', team_players_dict=team_players_dict)


@views.route('/process_player', methods=['GET', 'POST'])
def process_player():
    file_path = os.path.join(os.path.dirname(__file__), 'team_players_dict.pkl')
    with open(file_path, 'rb') as file:
        team_players_dict = pickle.load(file)

    selected_id = request.json.get('player_id')
    selected_stat = request.json.get('selected_stat')
    print("Selected stat: ", selected_stat)
    print(selected_id)

    # Retrieve dataframe containing player stats.
    player_df = player_log_df(selected_id, season)

    # Creating list of data based on the selected stat.
    if selected_stat == 'pts':
        stat_list = player_df['PTS'].head(15).to_list()
    elif selected_stat == 'ast':
        stat_list = player_df['AST'].head(15).to_list()
    elif selected_stat == 'reb':
        stat_list = player_df['REB'].head(15).to_list()
    elif selected_stat == 'pts-ast':
        pts_list = player_df['PTS'].head(15)
        ast_list = player_df['AST'].head(15)
        stat_list = (pts_list + ast_list).to_list()
    elif selected_stat == 'pts-reb':
        pts_list = player_df['PTS'].head(15)
        reb_list = player_df['REB'].head(15)
        stat_list = (pts_list + reb_list).to_list()
    elif selected_stat == 'reb-ast':
        reb_list = player_df['REB'].head(15)
        ast_list = player_df['AST'].head(15)
        stat_list = (reb_list + ast_list).to_list()
    elif selected_stat == 'pra':
        pts_list = player_df['PTS'].head(15)
        reb_list = player_df['REB'].head(15)
        ast_list = player_df['AST'].head(15)
        stat_list = (pts_list + ast_list + reb_list).to_list()
    elif selected_stat == 'threes':
        stat_list = player_df['FG3M'].head(15).to_list()

    date_list = player_df['GAME_DATE'].head(15).to_list()
    new_date_list = []
    for date in date_list:
        new_date_list.append(date[:10])
    data = {'dates': new_date_list, 'stats': stat_list}

    return jsonify(data)

