from ..models import Calendar, League


def insert_calendar(calendar_to_insert, league):
    current_calendar = Calendar.objects.filter(league=league)
    for match in calendar_to_insert:
        try:
            row = current_calendar.get(week=match.week)
            pass
        except:
            match.save()
    pass