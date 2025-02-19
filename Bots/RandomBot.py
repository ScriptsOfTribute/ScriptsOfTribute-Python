import random

from AIService.base_ai import BaseAI

class RandomBot(BaseAI):
    
    def select_patron(self, available_patrons):
        #print("RandomBot select patron")
        return random.choice(available_patrons)
    
    def play(self, game_state, possible_moves, remaining_time):
        # game_state.debug_print()
        pick = random.choice(possible_moves)
        return pick
    
    def game_end(self, final_state):
        pass