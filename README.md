# RLTrader
A script that trades stock through rocket league performance

## Description
The ``rl_reader.py`` pings your ballchasing account every 30s (change via line 80), 
when it finds a new game played, it takes the average team score (team branch, personal score for main) 
and normalizses it to pick 1 out of 1500 possible stock options on the NYSE/NASDAQ that are under $10

Your team(or personal) performance also determines the quantity to buy with better meaning more.

The script then purchases those stocks via the linked alpaca account. 

## Selling
Currently, there is a selling algorithm in ``sell_strat_basic_.py`` however it is untested and not a requirement/priority

## How to Use
**I recommend using the TEAM Branch as main is out of date and only accounts for individual performance**
- First clone the repo and install the following libraries
  - alpaca_trade_api
  - requests
  - pandas
- Create an ``api_keys.txt`` on the base layer
  - Line 1 should be your 20 character alpaca API key
  - Line 2 should be your **secret** alpaca API key
  - Line 3 should be your ballchasing.com api key
    - https://ballchasing.com/upload (the upload token)
- In ``rl_reader.py`` change the ``RL_Username`` variable to a string of your epic/steam rl username
- **NOTE**: The following steps will begin buying stocks, I reccomend linking to a paper account first, to let the software add all old replays to completed replays without spending real money.
- Run ``rl_reader.py`` it will create a ``completed_replays.txt`` if it does not exist
- When done playing, terminate the program.

## Terms of Use
This software is free and able to be used by anyone however should you wish to make content with it or share any part of it, I require you to credit me in at least one of the following ways:
- Reddit: u/TheLegoDude007
- Discord: Thoride#1618
  - discord.gg/marbles
- Github: Thoride-Dev
