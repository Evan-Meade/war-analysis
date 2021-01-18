import random
from uuid import uuid4
import pandas as pd
from war.models import Player


class WarGame:
    def __init__(self, suits=4, values=13, tie=2):
        """
        suits : number of repeats for each value
        values : number of unique values
        tie : number of cards put into the pile in the event of
              a tie, WITHOUT BEING FLIPPED
        """
        self.SUITS = suits
        self.VALUES = values
        self.TIE = tie

        self.reset()

    def reset(self):
        self.player0 = Player()
        self.player1 = Player()
        
        self.cards = [i for i in range(self.VALUES)] * self.SUITS
        random.shuffle(self.cards)
        n = round(len(self.cards)/2)
        self.player0.draw_pile = self.cards[0:n]
        self.player1.draw_pile = self.cards[n:]
        self.start0 = self.player0.draw_pile.copy()
        self.start1 = self.player1.draw_pile.copy()

        self.id = uuid4().hex
        self.status = 'ongoing'
        self.last_winner = -1
        self.last_win_value = -1
        self.last_loser = -1
        self.last_lose_value = -1
        self.last_pot_size = -1
        self.last_pot_value = -1
        self.turn = 1
        self.winner = -1
        self.valid_turn = False
        cols = ['id', 'turn_number', 'winner.player', 'winner.value', 'loser.player', 'loser.value', 'pot.size', 'pot.value',
                    'player0.size', 'player0.value', 'player1.size', 'player1.value']
        self.turn_data = pd.DataFrame(columns=cols)
    
    def compare_hands(self):
        top0 = self.player0.play_pile[-1]
        top1 = self.player1.play_pile[-1]

        if top0 > top1:
            self.last_winner = 0
            self.last_win_value = top0
            self.last_loser = 1
            self.last_lose_value = top1
            self.last_pot_size = len(self.player0.play_pile) + len(self.player1.play_pile)
            self.last_pot_value = sum(self.player0.play_pile) + sum(self.player1.play_pile)
            return 0
        elif top1 > top0:
            self.last_winner = 1
            self.last_win_value = top1
            self.last_loser = 0
            self.last_lose_value = top0
            self.last_pot_size = len(self.player0.play_pile) + len(self.player1.play_pile)
            self.last_pot_value = sum(self.player0.play_pile) + sum(self.player1.play_pile)
            return 1
        else:
            return -1
        
    def play_turn(self, nested=False):
        d0 = self.player0.draw()
        d1 = self.player1.draw()

        if d0 != 0:
            self.game_over(1)
            return None
        elif d1 != 0:
            self.game_over(0)
            return None

        result = self.compare_hands()
        if result == 0:
            self.player0.win(self.player1.play_pile)
            self.player1.lose()
            self.valid_turn = True
        elif result == 1:
            self.player1.win(self.player0.play_pile)
            self.player0.lose()
            self.valid_turn = True
        else:
            d0 = self.player0.draw(self.TIE)
            d1 = self.player1.draw(self.TIE)

            if d0 != 0:
                self.game_over(1)
                return None
            elif d1 != 0:
                self.game_over(0)
                return None
            self.play_turn(nested=True)

        if not nested and self.valid_turn:
            self.record_turn()
            self.turn += 1
        
        return None
    
    def record_turn(self):
        turn_stats = {
            'id': self.id,
            'turn_number': self.turn,
            'winner.player': self.last_winner,
            'winner.value': self.last_win_value,
            'loser.player': self.last_loser,
            'loser.value': self.last_lose_value,
            'pot.size': self.last_pot_size,
            'pot.value': self.last_pot_value,
            # 'player0.won': self.player0.won_pile,
            # 'player0.draw': self.player0.draw_pile,
            'player0.size': self.player0.num_cards(),
            'player0.value': self.player0.total_value(),
            # 'player1.won': self.player1.won_pile,
            # 'player1.draw': self.player1.draw,
            'player1.size': self.player1.num_cards(),
            'player1.value': self.player1.total_value()
        }
        turn_df = pd.DataFrame(turn_stats, index = [self.turn])
        self.turn_data = pd.concat([self.turn_data, turn_df])
    
    def game_over(self, winner):
        self.status = 'over'
        self.winner = winner
        # print(f'Game over, winner {winner} on turn {self.turn}')

    def play_game(self):
        while self.status != 'over':
            self.valid_turn = False
            self.play_turn()
    
    def game_dict(self):
        game_stats = {
            'id': self.id,
            'suits': self.SUITS,
            'values': self.VALUES,
            'tie': self.TIE,
            'winner': self.winner,
            'length': self.turn,
            # 'player0_start.hand': self.start0,
            'player0_start.size': len(self.start0),
            'player0_start.value': sum(self.start0),
            # 'player1_start.hand': self.start1,
            'player1_start.size': len(self.start1),
            'player1_start.value': sum(self.start1)
        }

        return game_stats