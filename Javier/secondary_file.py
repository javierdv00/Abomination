from Tables_are_fun import create_tables
from fifa_rank import fifa_rank
from player import players
from google import team_info
from Tables_are_fun import check_team

def run_secondary(run=True):
    if run:
        create_tables()
        print('tables created')
        fifa_rank()
        page = 1
        gender = 0
        max_page = 10
        while True:         # loop for male players
            players_output = players(gender=gender,page=page)
            if players_output =='No_table':
                print('break-male')
                break
            else:
                page += 1
                unique_teams = list(set(players_output))
                for team in unique_teams:
                    print(team, check_team(team))
                    if check_team(team) == False:
                        team_info(team)
                if page >= max_page:
                    print('max page - male')
                    break
                    
        page = 1
        gender = 1
        # while True:         # loop for female players
        #     players_output = players(gender=gender,page=page)
        #     if players_output =='No_table' or page >= max_page:
        #         print('break-female')
        #         break
        #     else:
        #         page += 1

    print('finish scrapping')
    