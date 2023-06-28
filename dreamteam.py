import os
import pandas as pd
import pulp as pl
import csv

from pulp.constants import LpMaximize
from pulp.pulp import lpSum
from pulp.utilities import value


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_result(a, b, c, d, e):
    result = 0.0
    result += (a*(30/100))
    result += (b*(25/100))
    result += (c*(20/100))
    result += (d*(15/100))
    result += (e*(10/100))
    return result

def LinearProgramming(player_name, features_dictionary):
    # SO THE FIRST THING IS TO DEFINE THE DESICION VARIABLE
    # IN THIS CASE THE VARIABLE ARE PLAYERS WHICH CAN HAVE 2 VALUES {0,1}
    # IF PLAYER VALUE IS 0 IT IMPLIES PLAYER IS NOT PICKED ELSE IT IS PICKED
    players_chosen=pl.LpVariable.dicts("Player chosen",player_name,0,1,cat='Integer')

    # OPTIMIZATION PROBLEM
    # WE NEED TO MAXIMISE THE TOTAL POINTS OF THE TEAM
    # TOTAL POINT HERE IS OPTIMIZER THAT IS CALCULATED FROM THE PERFORMANCE OF PLAYER IN LAST 5 MATCHES
    
    # INITIALIZE THE PROBLEM
    problem = pl.LpProblem("Fantasy Team", LpMaximize)

    # Optimised points of the team are the sum of optimizer of the chosen players

    problem += lpSum([features_dictionary['optimizer'][player]*players_chosen[player] for player in player_name]), "Maximize Optimizer"

    # CONSTRAINTS
    # 1ST THAT THE TOTAL PLAYERS CHOSEN NEED TO BE EXACTLY 11

    problem += lpSum(players_chosen[player] for player in player_name) == 11, "Total Player"

    # 2nd number of players from a given team need to at least 4 and at most 7
    problem += lpSum(features_dictionary['team1'][player]*players_chosen[player] for player in player_name) >= 4, "Team1 Minimum"
    problem += lpSum(features_dictionary['team1'][player]*players_chosen[player] for player in player_name) <= 7, "Team1 Maximum"
    problem += lpSum(features_dictionary['team2'][player]*players_chosen[player] for player in player_name) >= 4, "Team2 Minimum"
    problem += lpSum(features_dictionary['team2'][player]*players_chosen[player] for player in player_name) <= 7, "Team2 Maximum"

    # We need to select at least 1 wk
    # At least 3 batter
    # At least 3 bowler
    # At least 1 all rounder
    problem += lpSum(features_dictionary['wk'][player]*players_chosen[player] for player in player_name) >=1, "Minimum Wicket Keeper"
    
    problem += lpSum(features_dictionary['bat'][player]*players_chosen[player] for player in player_name) >=3, "Minimum Batter"
    
    problem += lpSum(features_dictionary['bowl'][player]*players_chosen[player] for player in player_name) >=3, "Minimum Bowlers"
    
    problem += lpSum(features_dictionary['ar'][player]*players_chosen[player] for player in player_name) >=1, "Minimum All rounder"
    
    # We need to select maximum 4 wk
    # at most 6 batter
    # at most 6 bowler
    # at most 4 all rounder
    problem += lpSum(features_dictionary['wk'][player]*players_chosen[player] for player in player_name) <=4, "Maximum Wicket Keeper"
    problem += lpSum(features_dictionary['bat'][player]*players_chosen[player] for player in player_name) <=6, "Maximum Batter"
    
    # We need to select at least 1 all rounder and at most 6 all rounder
    problem += lpSum(features_dictionary['bowl'][player]*players_chosen[player] for player in player_name) <=6, "Maximum Bowlers"
    problem += lpSum(features_dictionary['ar'][player]*players_chosen[player] for player in player_name) <=4, "Maximum All rounder"

    problem.solve()
    print("Status:", pl.LpStatus[problem.status])
    # prob.solver
    
    print("ROI maximized = {}".format(round( value(problem.objective) ,2)))
    return problem

if __name__ == '__main__':
    print(bcolors.OKCYAN + "\t\t Welcome to Make your dream team" + bcolors.ENDC)
    print(bcolors.WARNING + "This is based on linear programming and recent form Use this at your own risk" + bcolors.ENDC)
    file_location = input(
        bcolors.OKGREEN + "Please Enter the locaton of file" + bcolors.ENDC)
    try:
        f = open(file_location, "r")
    except FileNotFoundError:
        print(bcolors.FAIL + "Given file not found" + bcolors.ENDC)
        exit
    f.close()
    file_name = os.path.basename(file_location)
    headers = []
    rows = []
    team_name_1 = "-"
    team_name_2 = "-"
    with open(file_location, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # headers is a list that contains the first row of csv
        headers = next(csvreader)
        i = 0
        # for field in headers:
        #     if(field[0] == "previous"):
        #     i += 1
        # Assume i get data for 5 matches
        headers.append("Optimizer")
        for row in csvreader:
            # row contains the ith row of csv file
            result = get_result(float(row[3]), float(row[4]), float(
                row[5]), float(row[6]), float(row[7]))
            if(team_name_1 == "-"):
                team_name_1 = row[1]
            elif(team_name_1 != row[1] and team_name_2 == "-"):
                team_name_2 = row[1]
            row.append(result)  # adding the answer in row
            rows.append(row)  # adding the row to the list of lists
    # print(headers)
    # print(rows)
    #print(team_name_1 + " " + team_name_2)
    '''
        Now need to form a dictionary
        keys credits bat bowl ar wk team1 team2 optimizer
        value of dictionary will be a dictionary
            for that dictionary
            key - player name
            value - value for that particular field
    '''
    feature_cols = ['credits', 'optimizer',  'team1', 'team2','ar', 'bat', 'bowl', 'wk']
    features_dictionary = {}
    for col in feature_cols:
        features_dictionary[col] = dict()
    player_name=[]
    for i in rows:
        player_name.append(i[0])
        features_dictionary['credits'][i[0]]=i[8]
        features_dictionary['optimizer'][i[0]]=i[9]
        if(team_name_1==i[1]):
            features_dictionary['team1'][i[0]]=1
            features_dictionary['team2'][i[0]]=0
        else:
            features_dictionary['team1'][i[0]]=0
            features_dictionary['team2'][i[0]]=1
        if(i[2]=='BAT'):
            features_dictionary['bat'][i[0]]=1
            features_dictionary['wk'][i[0]]=0
            features_dictionary['ar'][i[0]]=0
            features_dictionary['bowl'][i[0]]=0
        elif(i[2]=='BOWL'):
            features_dictionary['bat'][i[0]]=0
            features_dictionary['wk'][i[0]]=0
            features_dictionary['ar'][i[0]]=0
            features_dictionary['bowl'][i[0]]=1
        elif(i[2]=='WK'):
            features_dictionary['bat'][i[0]]=0
            features_dictionary['wk'][i[0]]=1
            features_dictionary['ar'][i[0]]=0
            features_dictionary['bowl'][i[0]]=0
        else:
            features_dictionary['bat'][i[0]]=0
            features_dictionary['wk'][i[0]]=0
            features_dictionary['ar'][i[0]]=1
            features_dictionary['bowl'][i[0]]=0

    # print(features_dictionary)
    Problem = LinearProgramming(player_name,features_dictionary)

    # Let me create a list of chosen players
    players_selected=[]
    playerAndOptimizer={}
    for players in Problem.variables():
        if(players.varValue>0):
            new_string = players.name.replace("_", " ")
            new_string = new_string.replace("Player chosen ","")
            players_selected.append(new_string)
            playerAndOptimizer[new_string]=features_dictionary['optimizer'][new_string]
    # print(players_selected)
    count=1
    print(bcolors.OKGREEN + "Selected players are :")
    for playesr in players_selected:
        print(bcolors.OKBLUE + count,"\t",playesr + bcolors.ENDC)
    sort_order = sorted(playerAndOptimizer.items(), key=lambda x: x[1] , reverse=True)
    sort_order2=dict(sort_order)
    j=0
    for key in sort_order2:
        if(j==0):
            print("The optimised choice for captain is " , key)
        if(j==1):
            print("The optimised choice for vice-captain is ", key)
        j+=1
    # need to create a new output file
    try:
        os.mkdir('Outputs')
    except FileExistsError:
        print()
    output_file = "Outputs/result_" + file_name
    with open(output_file,'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        for row in rows:
            if( row[0] in players_selected):
                csvwriter.writerow(row)