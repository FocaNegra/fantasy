from string import punctuation
from bs4 import BeautifulSoup
import requests
import datetime
from fcf_functions import *


def get_calendar(url):
    # Creates a list with dictionaries for each week. Keys are:
    # week, season, game_date, url, status, oponent, team_enddate, punctuation_enddate, next_update

    soup = get_soup_from_url(url)
    calendar = get_calendar_data_from_calendar_soup(soup)
    return calendar
