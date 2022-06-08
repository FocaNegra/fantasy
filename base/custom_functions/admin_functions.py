from calendar import week
from .fcf_functions import *
from ..models import Calendar


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
