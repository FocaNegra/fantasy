from ..models import Calendar, League, Player, Region_Group, Region_Team

def update_calendar_status(calendar, status:str):

    avalaible_status = [
        "waiting",
        "next",
        "locked",
        "punctuating",
        "closed"
    ]

    if status in avalaible_status:
        calendar.status = status
        calendar.save()
        print(f"     Calendar status changed to {status}")
    else:
        print(f"     Status '{status}' does not exist.")

def update_calendar_dates(league):
    pass