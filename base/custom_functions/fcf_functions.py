from bs4 import BeautifulSoup
import requests
import datetime
import pytz

timezone = pytz.timezone("Europe/Madrid")

def get_soup_from_url(url):
    # input: url del equip a la fcf.
    # output: soup per fer el web scrapping.
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    return soup

def get_url_dicc_from_team(team):
    team_urls = {"urlTeam":"https://www.fcf.cat/equip/2022/3cat/%s" % team,
                "urlSchedule" : "https://www.fcf.cat/calendari-equip/2022/futbol-11/tercera-catalana/grup-6/%s" % team}
    return team_urls

def get_all_players_list_from_team_soup(soup):
    playerList = []
    mainColumn = soup.find_all('div', class_='col-md-4')
    playerTable = mainColumn[1].find('table', class_="fcftable w-100 mb-20").find_all('td')
    for player in playerTable:
        playerList.append(player.text.strip())
    return playerList

def normalize_player_names(player_list, region):
    output_list = []
    if region == 'fcf':
        for match_report_name in player_list:
            if "," in match_report_name:
                last_name = match_report_name.split(", ")[0].lower()
                name = match_report_name.split(", ")[1].lower()
            else:
                name = match_report_name.lower()
                last_name = ""
            player_dict = {
                'name': name,
                'last_name': last_name,
                'alias': "",
                'match_report_name': match_report_name,
            }
            output_list.append(player_dict)
    else:
        raise Exception("The system is not ready to normaliza player data from other regions than 'fcf'")
    return output_list

def get_team_name_from_calendar_soup(soup):
    return soup.find('p', class_ = 'm-0 fs-30 va-b bold').text.strip()

def get_calendar_data_from_calendar_soup(soup):
    calendarData = []
    calendarTable = soup.find('table', class_='fcftable w-100 fs-12_ml').find_all('tr')[1:]
    teamName = soup.find('p', class_="m-0 fs-30 va-b bold").getText()

    for row in calendarTable:
        jornada = row.find_all('td', class_='tc')[0].text
        dia_partit = row.find_all('td', class_='tc')[1].text
        hora_partit = row.find_all('td', class_='tc')[2].text
        data_partit = datetime.datetime(int(dia_partit[6:]), int(dia_partit[3:5]), int(dia_partit[:2]),
                                        int(hora_partit[1:3]), int(hora_partit[4:6]))
        data_partit = timezone.localize(data_partit).astimezone(pytz.utc)
        timedelta_team_submit = datetime.timedelta(hours=-2)
        enddate_for_team_submit = data_partit + timedelta_team_submit
        timedelta_punctuation = datetime.timedelta(days=2)
        enddate_for_punctuation = data_partit + timedelta_punctuation
        timedelta_update = datetime.timedelta(hours=2)
        next_update = data_partit + timedelta_update
        resultat = row.find_all('td', class_='tc')[3].text
        equip_local = row.find_all('td', class_='tl')[0].text
        equip_visitant = row.find_all('td', class_='tl')[1].text
        if equip_local == teamName:
            equip_contrari = equip_visitant
            is_local = True
        else:
            equip_contrari = equip_local
            is_local = False
        try:
            url_acta_partit = row.find_all('td', class_='tc')[3].find('a', href=True)['href']
            status = 'open'
        except:
            url_acta_partit = 'none'
            status = 'undisputed'

        report = {
            'week': jornada,
            'season': '2021-2022',
            'game_date': data_partit,
            'result': resultat,
            'url': url_acta_partit,
            'status':status,
            'oponent': equip_contrari,
            'hosting': is_local,
            'team_enddate': enddate_for_team_submit,
            'punctuation_enddate': enddate_for_punctuation,
            'next_update': next_update,
        }
        listToAdd = report
        calendarData.append(listToAdd)

    return(calendarData)

def is_acta_closed(soup):
    return soup.find('div', class_='acta-estat').text.strip() == "ACTA TANCADA"

def get_acta_tables_from_acta_soup(soup):
    main_columns = soup.find_all('div', class_='col-md-4 p-0_ml')
    table_local = main_columns[0].find_all('table', class_="acta-table")
    table_local_subs = main_columns[0].find('table', class_="acta-table2")
    table_visitant = main_columns[2].find_all('table', class_="acta-table")
    table_visitant_subs = main_columns[2].find('table', class_="acta-table2")
    tables = ["table_local_starters","table_local_subs","table_local_substitutions","table_local_cards",
              "table_visitant_starters","table_visitant_subs","table_visitant_substitutions", "table_visitant_cards"]
    acta_tables = {}
    for table in tables:
        if table == "table_local_starters":
            try:
                acta_tables[table] = table_local[0]
            except:
                acta_tables[table] = ""
        elif table == "table_local_subs":
            try:
                acta_tables[table] = table_local[1]
            except:
                acta_tables[table] = ""
        elif table == "table_local_substitutions":
            try:
                acta_tables[table] = table_local_subs
            except:
                acta_tables[table] = ""
        elif table == "table_local_cards":
            try:
                acta_tables[table] = table_local[3]
            except:
                acta_tables[table] = ""
        elif table == "table_visitant_starters":
            try:
                acta_tables[table] = table_visitant[0]
            except:
                acta_tables[table] = ""
        elif table == "table_visitant_subs":
            try:
                acta_tables[table] = table_visitant[1]
            except:
                acta_tables[table] = ""
        elif table == "table_visitant_substitutions":
            try:
                acta_tables[table] = table_visitant_subs
            except:
                acta_tables[table] = ""
        elif table == "table_visitant_cards":
            try:
                acta_tables[table] = table_visitant[3]
            except:
                acta_tables[table] = ""
    return acta_tables

def read_acta_stats_from_player(stats_soup):
    goals, penalty_goal, own_goals, yellow_cards, red_cards = 0, 0, 0, 0, 0
    for item in stats_soup:
        if item.find('div')['class'] == ['gol']:
            stat = item.find('div').find('div')['class'][3]
        else:
            stat = item.find('div')['class'][0]
        try:
            comptador = int(item.find('div', class_='comptador').text)
        except:
            comptador = 1

        if stat == 'gol-normal':
            goals = comptador
        elif stat == 'gol-penal':
            penalty_goal = comptador
        elif stat == 'gol-propia':
            own_goals = comptador
        elif stat == 'groga-s':
            yellow_cards = comptador
        elif stat == 'vermella-s':
            red_cards = comptador

    return goals, penalty_goal, own_goals, yellow_cards, red_cards

def get_player_stats_from_table(soup, is_starter):
    output_list = []

    for player in soup.find('tbody').find_all('tr'):
        dorsal = int(player.find_all('td')[0].find('span', class_='num-samarreta-acta2').text)
        player_name = player.find('a').text
        jersey_color = player.find('span', class_='p-a faf-base')['style']
        acta_stats_soup = player.find_all('div', class_='acta-stat-box')
        goals, penalty_goal, own_goals, yellow_cards, red_cards = read_acta_stats_from_player(acta_stats_soup)
        start_minute = None
        final_minute = None
        if is_starter:
            start_minute = 0
            final_minute = 90

        output_list.append({
            "dorsal": dorsal,
            "player_name": player_name,
            "jersey_color": jersey_color,
            "is_starter": is_starter,
            "start_minute": start_minute,
            "final_minute": final_minute,
            "goals": goals,
            "penalty_goal": penalty_goal,
            "own_goals": own_goals,
            "yellow_cards": yellow_cards,
            "red_cards": red_cards,
        })
    return output_list

def get_jersey_positions_using_color(player_data):
    color1 = ''
    count1 = 0
    color2 = ''
    count2 = 0
    for player in player_data:
        if color1 == '':
            color1 = player["jersey_color"]
            count1 += 1
        elif color1 == player["jersey_color"]:
            count1 += 1
        elif color2 == '':
            color2 = player["jersey_color"]
            count2 += 1
        else:
            count2 += 1
    if count1 >= count2:
        jersey_color_dicc = {
            color1: False,
            color2: True
        }
    else:
        jersey_color_dicc = {
            color1: True,
            color2: False
        }
    return jersey_color_dicc

def replace_color_by_position(player_data, jersey_color_dicc):
    for player in player_data:
        player["is_goalkeeper"] = jersey_color_dicc[player["jersey_color"]]
    return player_data

def get_subtitution_list(taula_substitucions):
    tbody = taula_substitucions.find('tbody')
    n = 0
    tr = tbody.find_all('tr')
    list_substitucions = []

    while n < len(tr) - 1:
        minut = int(tr[n].find('td', rowspan='2').text[:-1])
        surt = tr[n].find('a').text
        entra = tr[n + 1].find('a').text
        n = n + 2
        list_substitucions.append(
            {
                "minut" : minut,
                "surt": surt,
                "entra": entra,
            })

    return list_substitucions

def send_off_data(cards_table):
    output_list = []

    if cards_table != "":
        for incident in cards_table.find('tbody').find_all('tr'):
            name = incident.find('a').text
            minute_str = incident.find('div', class_="acta-minut-targeta").text[:-1]
            if minute_str == "":
                minute = 90
            else:
                minute = int(minute_str)
            output_list = [[minute, name]] + output_list

    return output_list

def get_send_off_players(player_data):
    send_off_players = []
    for player in player_data:
        if (player["yellow_cards"] > 1 or player["red_cards"] > 0):
            send_off_players.append(player["player_name"])

    return send_off_players

def add_send_off_to_subs_list(send_off_players, send_off_data, subs_list):
    if send_off_players:
        for player in send_off_players:
            player_name = player
            if send_off_data:
                for incident in send_off_data:
                    if player == incident[1]:
                        minute = incident[0]
                        subs_list.append(
                            {
                                "minut": minute,
                                "surt": player_name,
                                "entra": ""
                            })
                        break
    return subs_list


def update_data_with_substitutions(player_data, substitution_list):

    for sub in substitution_list:
        for player in player_data:
            if player["player_name"] == sub["surt"]:
                player["final_minute"] = sub["minut"]
            if player["player_name"] == sub["entra"]:
                player["start_minute"] = sub["minut"]
                player["final_minute"] = 90
    return player_data

def update_data_with_total_minutes(player_data):
    for player in player_data:
        if player["start_minute"] == None:
            player["mins_played"] = 0
        else:
            player["mins_played"] = player["final_minute"] - player["start_minute"]

    return player_data

def get_full_data_from_acta(url, is_local):

    sopa = get_soup_from_url(url)

    if is_acta_closed(sopa):
        data_acta = get_acta_tables_from_acta_soup(sopa)

        if is_local:
            sopa_titulars = data_acta["table_local_starters"]
            sopa_suplents = data_acta["table_local_subs"]
            sopa_incidents = data_acta["table_local_cards"]            
            sopa_substitucions = data_acta["table_local_substitutions"]
        else:
            sopa_titulars = data_acta["table_visitant_starters"]
            sopa_suplents = data_acta["table_visitant_subs"]
            sopa_incidents = data_acta["table_visitant_cards"]            
            sopa_substitucions = data_acta["table_visitant_substitutions"]

        player_data_titulars = get_player_stats_from_table(sopa_titulars, True)
        color_dicc = get_jersey_positions_using_color(player_data_titulars)
        replace_color_by_position(player_data_titulars, color_dicc)

        player_data_suplents = get_player_stats_from_table(sopa_suplents, False)
        replace_color_by_position(player_data_suplents, color_dicc)
        player_data = player_data_titulars + player_data_suplents

        send_off_players = get_send_off_players(player_data)
        cards_data = send_off_data(sopa_incidents)
        subs_list = get_subtitution_list(sopa_substitucions)

        subs_list = add_send_off_to_subs_list(send_off_players, cards_data, subs_list)

        update_data_with_substitutions(player_data, subs_list)
        updated_data = update_data_with_total_minutes(player_data)

        print(cards_data)
        print(subs_list)

        print(updated_data)
        return updated_data

    else:
        return [[]]

def get_groups_from_category(category, list = []):

    soup = BeautifulSoup(category['html_div'], 'lxml')
    html_group_list = soup.find_all('a', class_="grupo")
    for group in html_group_list:
        group_name = group.find('p').get_text()
        group_url = group['href']
        list.append({'category': category['name'], 'group_name': group_name, 'group_url': group_url, 'standings_url': group_url.replace('resultats','classificacio')})
    return list

def get_teams_from_group(group_class):
    list = []
    soup = get_soup_from_url(group_class.standing_url)
    team_rowlist = soup.find('table', class_="fcftable-e w-100 fs-12_tp fs-11_ml").find_all('tr')[2:]
    for team in team_rowlist:
        try:
            team_name = team.find('td',  class_='tl resumida').find('a', href=True).get_text()
            schedule_url = team.find('td',  class_='tl resumida').find('a', href=True)['href']
            team_url = team.find('td', class_="tc pr-0").find('a', href=True)['href']
            alias = schedule_url.split('/')[-1]
            list.append({'team_name': team_name, 'schedule_url': schedule_url, 'team_url': team_url, 'alias': alias, 'region_group': group_class})
        except:
            pass
    return list