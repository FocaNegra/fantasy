from .admin_functions import *
from .insert_functions import *
from .update_functions import *

def initialize_calendar(calendar):
    print(f"({calendar.week}) initializing calendar for {calendar.week}")

    update_calendar_status(calendar, "locked")
    match_report = get_match_report(calendar)

    insert_match_report(match_report["match_report"], calendar)
    
    update_calendar_status(calendar, "punctuating")
    update_calendar_status(calendar, "closed")


def initialize_league_sync(league):
    print("initializing league")

    calendar_list = Calendar.objects.filter(league=league, status="open").order_by("game_date")

    while len(calendar_list) >= 1:
        update_calendar_dates(league)
        calendar_list = Calendar.objects.filter(league=league, status="open").order_by("game_date")
        next_calendar = get_next_calendar(league)
        initialize_calendar(next_calendar)




