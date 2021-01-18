import random


class Player:
    def __init__(self):
        self.draw_pile = []
        self.won_pile = []
        self.play_pile = []
    
    def __repr__(self):
        s = f'\nDraw pile: {self.draw_pile}\n'
        s += f'Won pile: {self.won_pile}\n'
        s += f'Play pile: {self.play_pile}\n\n'
        return s
    
    def num_cards(self):
        return len(self.draw_pile) + len(self.won_pile) + len(self.play_pile)
    
    def total_value(self):
        return sum(self.draw_pile) + sum(self.won_pile) + sum(self.play_pile)

    def draw(self, n=1):
        for i in range(n):
            if len(self.draw_pile) == 0:
                self.shuffle()
                if len(self.draw_pile) == 0:
                    return None
            self.play_pile = self.play_pile + self.draw_pile[-1:]
            self.draw_pile = self.draw_pile[:-1]
        return 0
    
    def shuffle(self):
        random.shuffle(self.won_pile)
        self.draw_pile = self.draw_pile + self.won_pile
        self.won_pile = []
    
    def lose(self):
        self.play_pile = []
    
    def win(self, pot=[]):
        self.won_pile = self.won_pile + self.play_pile + pot
        self.play_pile = []
