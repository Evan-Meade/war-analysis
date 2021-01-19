import os
import sys
import time
import concurrent.futures
import pandas as pd
from war import WarGame


NUM = int(sys.argv[1])
SUITS = int(sys.argv[2])
VALUES = int(sys.argv[3])
TIE = int(sys.argv[4])
PREFIX = sys.argv[5]

print(f'Simulating {NUM} games with {SUITS} suits, {VALUES} values, and {TIE} unflipped cards per tie...')

def simulate(n, s, v, t):
    wg = WarGame(s, v, t)
    war_game_data = pd.DataFrame()
    war_turn_data = pd.DataFrame()

    for i in range(n):
        wg.reset()
        wg.play_game()

        game_data = wg.game_dict()
        game_df = pd.DataFrame(game_data, index=[i])
        war_game_data = pd.concat([war_game_data, game_df])
        
        war_turn_data = pd.concat([war_turn_data, wg.turn_data])
    
    return war_game_data, war_turn_data
#     return True

master_game_data = pd.DataFrame()
master_turn_data = pd.DataFrame()

N_CPU = os.cpu_count()
nums = [NUM // N_CPU] * N_CPU
for i in range(NUM % N_CPU):
    nums[i] += 1
params = [[nums[i], SUITS, VALUES, TIE] for i in range(N_CPU)]

with concurrent.futures.ProcessPoolExecutor() as executor:
#     results = [executor.submit(simulate, params[i]) for i in range(N_CPU)]
#     for result in concurrent.futures.as_completed(results):
#         print(result)
    results = executor.map(simulate, params)
    for result in results:
        master_game_data = pd.concat([master_game_data, result[0]])
        master_turn_data = pd.concat([master_turn_data, result[1]])

master_game_data.to_csv(f'{prefix}_game_data.csv', index=False)
master_turn_data.to_csv(f'{prefix}_turn_data.csv', index=False)

print(f'Simulated {n} games in {stop - start} seconds')
