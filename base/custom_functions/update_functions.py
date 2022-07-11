from ..models import Calendar, League, Player, Region_Group, Region_Team

def set_calendar_status(calendar, status:str):

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
        print(f"Calendar {calendar.id} status changed to {status}")
    else:
        print(f"Status '{status}' does not exist.")
