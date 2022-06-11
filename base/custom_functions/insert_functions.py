from ..models import Calendar, League, Player, Region_Group, Region_Team


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

def insert_region_groups(region_group_to_insert, region):
    groups_in_our_db = Region_Group.objects.filter(region=region)
    for group in region_group_to_insert:
        n = 0
        i = 0
        try:
            row = groups_in_our_db.get(group_url=group.group_url)
            i+=1
            pass
        except:
            group.save()
            n += 1
    pass

def insert_region_teams(region_team_to_insert):
    
    for group_dict in region_team_to_insert:
        group_category = group_dict['group'].category
        group_name = group_dict['group'].group_name
        group_filt = Region_Group.objects.filter(category=group_category)
        group = group_filt.get(group_name=group_name)
        print(f"adding {group}")
        team_list = group_dict['list_teams']
        teams_in_our_db = Region_Team.objects.filter(region_group=group)
        n=0  
        for team in team_list:         
            try:
                row = teams_in_our_db.get(alias=team.alias)
                pass
            except:
                team.region_group = group
                team.save()           
                n+=1
                print('--- saving', team)
        print(f"---> Added {n} teams in {group}\n\n")
    pass