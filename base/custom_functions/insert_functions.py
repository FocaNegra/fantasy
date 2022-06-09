from ..models import Calendar, League, Player


def insert_calendar(calendar_to_insert, league):
    current_calendar = Calendar.objects.filter(league=league)
    for match in calendar_to_insert:
        try:
            row = current_calendar.get(week=match.week)
            pass
        except:
            match.save()
    pass

def insert_players(players_to_insert, league):
    players_in_our_db = Player.objects.filter(league=league)
    for player in players_to_insert:
        try:
            row = players_in_our_db.get(match_report_name=player.match_report_name)
            pass
        except:
            player.save()
    pass