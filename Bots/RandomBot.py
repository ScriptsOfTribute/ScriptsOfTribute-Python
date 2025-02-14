import random

from AIService.base_ai import BaseAI

class RandomBot(BaseAI):
    
    def select_patron(self, available_patrons):
        print("RandomBot select patron")
        return random.choice(available_patrons)
    
    def play(self, game_state, possible_moves):
        # game_state.debug_print()
        return random.choice(possible_moves)
    
    def game_end(self, final_state):
        pass