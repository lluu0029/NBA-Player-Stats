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
    print(selected_id)
    player_df = player_log_df(selected_id, season)
    pts_list = player_df['PTS'].head(15).to_list()
    print(pts_list)
    date_list = player_df['GAME_DATE'].head(15).to_list()
    new_date_list = []
    for date in date_list:
        new_date_list.append(date[:10])
    data = {'dates': new_date_list, 'stats': pts_list}

    return jsonify(data)
    # return render_template('graph.html', pts=pts_list, date=date_list, team_dict=team_dict,
    #                         team_players_dict=team_players_dict)
