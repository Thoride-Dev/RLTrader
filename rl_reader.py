import time
import requests
from pick_stock import pick_stock
from trader import make_trade

#read api keys text file
with open('api_keys.txt', 'r') as f:
    api_keys = f.read().splitlines()

#read completed_replays.txt and add each line to set
with open('completed_replays.txt', 'r') as f:
    completed_replays = set(f.read().splitlines())


token = api_keys[2] #ballchasing.com token

RL_Username = "Thoride"


while True:
    url = "https://ballchasing.com/api/replays"
    PARAMS = {'player-name': RL_Username, 'count': 1, 'uploader':'me'}

    r = requests.get(url, params=PARAMS, headers={'Authorization':token})
    data = r.json()
    print("Pinging ballchasing.com...")

    #make sure we don't buy a stock twice
    if(data['list'][0]['id'] not in completed_replays):
        #add replay to completed_replays.txt
        completed_replays.add(data['list'][0]['id'])
        with open('completed_replays.txt', 'a') as f:
            f.write(data['list'][0]['id'] + '\n')
        
        print("New replay found!")
        #collect team data and init variables
        blue_team = data["list"][0]["blue"]["players"]
        orange_team = data["list"][0]["orange"]["players"]
        team_score = 0
        win = False
        try:
            blue_score = data['list'][0]['blue']['goals']
        except:
            blue_score = 0
        try:
            orange_score = data['list'][0]['orange']['goals']
        except:
            orange_score = 0

        #search for me in the team data and get my score
        for i in range(len(blue_team)):
            if blue_team[i]["name"] == RL_Username:
                for i in range(len(blue_team)): #another for loop to get team score
                    team_score += blue_team[i]["score"]
                if(blue_score > orange_score):
                    win = True
                break
            elif orange_team[i]["name"] == RL_Username:
                for i in range(len(orange_team)):
                    team_score += orange_team[i]["score"]
                if(orange_score > blue_score):
                    win = True
                break

        #average team score
        avg_team_score = team_score / len(blue_team)

        #loss penalty
        if(not win):
            avg_team_score = avg_team_score - 50
            print("Loss penalty applied.")

        #pick a stock based on my score and make a trade
        print("Avg team score: ", avg_team_score)
        stock_to_buy = pick_stock(avg_team_score)
        make_trade(stock_to_buy, avg_team_score)
    else:
        print("No new replay found.")
        
    time.sleep(30)