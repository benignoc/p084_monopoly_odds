# src/p084_monopoly_odds/monopoly.py

from random import shuffle
from random import randint
from collections import defaultdict

import multiprocessing as mp


COMMUNITY = [0, 10] + [None]*14
shuffle(COMMUNITY)
CHANCE = [0, 10, 11, 24, 39, 5, 'R', 'R', 'U', -3] + [None]*6
shuffle(CHANCE)
BOARD = [None, None, 'CC', None, None, 'R', None, 'CH', None, None, 
         None, None,  'U',  None,  None, 'R', None, 'CC', None, None,
         None, None, 'CH', None, None, 'R', None, None, 'U', None,
         10, None, None, 'CC', None, 'R', 'CH', None, None, None] 
         
DICE_SIDES = 4
PROCESSORS = mp.cpu_count()

class Player:
    def __init__(self):
        self.pos = 0
        self.hist = defaultdict(int)
    
    def _setpos(self, new_pos):
        self.pos = new_pos
    
    def roll(self) -> int:
        d1, d2 = randint(1, DICE_SIDES), randint(1, DICE_SIDES)
        n_rolls = 1
        self.move(d1 + d2)
        while d1 == d2 and n_rolls < 3:
            d1, d2 = randint(1, DICE_SIDES), randint(1, DICE_SIDES)
            n_rolls += 1
            if n_rolls == 3 & d1 == d2:
                # if three doubles goto jail
                self.pos = 10
                self.hist[10] += 1
            else:
                self.move(d1 + d2)
    
    def chance(self, pos):
        # Rotate CHANCE
        card = CHANCE.pop(0)
        CHANCE.append(card)
        if card is None:
            new_pos = pos
        elif type(card) == int:
            if card >= 0:
                new_pos = card
            else:
                new_pos = pos + card
        else: # card in ['R','U']:
            # index 0 is current position.
            b = BOARD[pos:] + BOARD[:pos]
            new_pos = (pos + b.index(card)) % len(BOARD)
        return new_pos

    def community_chest(self, pos):
        # Rotate COMMUNITY
        card = COMMUNITY.pop(0)
        COMMUNITY.append(card)
        if card == None:
            new_pos = pos
        else:
            new_pos = card
        return new_pos


    def check_redirects(self, pos):
        square = BOARD[pos]
        if square == 'CC':
            new_pos = self.community_chest(pos)
        elif square == 'CH':
            new_pos = self.chance(pos)
        elif type(square) == int:
            new_pos = square
        else:
            new_pos = pos
        return new_pos


    def move(self, roll):
        new_pos = (self.pos + roll) % len(BOARD)
        new_pos = self.check_redirects(new_pos)
        self.pos = new_pos
        self.hist[new_pos] += 1

def main():
    print(type(CHANCE))
    p = Player()
    for n in range(500000):
        p.roll()
    total = sum(p.hist.values())
    d = {k: round(100*v/total, 3) for k, v in sorted(p.hist.items(), key=lambda item: item[1])}
    print(d)