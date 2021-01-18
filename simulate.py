import sys
import time
import pandas as pd
from war import WarGame


n = int(sys.argv[1])
suits = int(sys.argv[2])
values = int(sys.argv[3])
tie = int(sys.argv[4])
prefix = sys.argv[5]

print(f'Simulating {n} games with {suits} suits, {values} values, and {tie} unflipped cards per tie...')

wg = WarGame(suits, values, tie)
war_game_data = pd.DataFrame()
war_turn_data = pd.DataFrame()

start = time.time()

for i in range(n):
    wg.reset()
    wg.play_game()

    game_data = wg.game_dict()
    game_df = pd.DataFrame(game_data, index=[i])
    war_game_data = pd.concat([war_game_data, game_df])
    
    war_turn_data = pd.concat([war_turn_data, wg.turn_data])

stop = time.time()

war_game_data.to_csv(f'{prefix}_game_data.csv', index=False)
war_turn_data.to_csv(f'{prefix}_turn_data.csv', index=False)

print(f'Simulated {n} games in {stop - start} seconds')
