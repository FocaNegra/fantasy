from calendar import week
from .fcf_functions import *
from ..models import Calendar, Player, Region_Group, Region_Team


def get_calendar(league):
    # Creates a list with dictionaries for each week. Keys are:
    # week, season, game_date, url, status, oponent, hosting, team_enddate, punctuation_enddate, next_update
    output_class_list = []
    url = league.schedule_url
    soup = get_soup_from_url(url)
    calendar = get_calendar_data_from_calendar_soup(soup)
    for row in calendar:
        c = Calendar(
            week = row['week'],
            season = row['season'],
            game_date = row['game_date'],
            result = row['result'],
            url = row['url'],
            status = row['status'],
            league = league,
            oponent = row['oponent'],
            hosting = row['hosting'],
            team_enddate = row['team_enddate'],
            punctuation_enddate = row['punctuation_enddate'],
            next_update = row['next_update']
        )
        output_class_list.append(c)
        
    return output_class_list

def update_model(model_to_update, new_model):
    pass

def get_players(league):
    output_class_list = []
    url = league.team_url    
    soup = get_soup_from_url(url)
    player_list = get_all_players_list_from_team_soup(soup)
    playerobj_list = normalize_player_names(player_list, 'fcf')
    for plobj in playerobj_list:
        p = Player(
            name = plobj['name'],
            last_name = plobj['last_name'],
            alias = plobj['alias'],
            match_report_name = plobj['match_report_name'],
            league = league,
            position = None,
            jersey_number = None,
        )
        output_class_list.append(p)

    return output_class_list

def get_region_groups(competitions_to_add, region):
    group_list = []
    output_class_list = []
    for category in competitions_to_add:
        group_list = get_groups_from_category(category, group_list)
        for group in group_list:
            g = Region_Group(
                region = region,
                category = group['category'],
                group_name = group['group_name'],
                group_url = group['group_url'],
                standing_url = group['standings_url'],
            )
            output_class_list.append(g)

    return output_class_list

def get_teams_from_groups(group_list):
    output_dict_list = []
    for group in group_list:
        group_dict = {'group': group}
        teams_list = []
        team_list = get_teams_from_group(group)
        for team_item in team_list:
            t = Region_Team(
                name = team_item['team_name'],
                schedule_url = team_item['schedule_url'],
                team_url = team_item['team_url'],
                alias = team_item['alias'],
            )
            teams_list.append(t)
        group_dict['list_teams'] = teams_list
        output_dict_list.append(group_dict)
    return output_dict_list
