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

def update_player_changes(player_change_list, players):
    # [{'id': '51', 'alias': '', 'position': '', 'number': ''}, ...]

    log_player_changes = {}

    for player_changed in player_change_list:
        if players.filter(id=player_changed['id']).exists():
            change_dict = {}
            player = players.get(id=player_changed['id'])
            player_before = {
                "alias" : player.alias,
                "position": player.position,
                "jersey_number": player.jersey_number,
            }            
            has_changed = { 
                "id": player.id,
                "alias" : player.alias == player_changed['alias'],
                "position": player.position == player_changed['position'],
                "jersey_number": player.jersey_number == player_changed['number'],
            }
            if not has_changed["alias"]:
                player.alias = player_changed['alias']
                change_dict["alias"] = {"old": player_before["alias"], "new":player_changed['alias']}
            if not has_changed["position"]:
                player.position = player_changed['position']
                change_dict["position"] = {"old": player_before["position"], "new":player_changed['position']}
            if not has_changed["jersey_number"]:
                player.alias = player_changed['number']
                change_dict["jersey_number"] = {"old": player_before["jersey_number"], "new":player_changed['number']}
            player.save()
            
            if change_dict != {}:
                change_dict["id"] = player.id
                log_player_changes[f"player-{player.id}"] = change_dict
    return log_player_changes
