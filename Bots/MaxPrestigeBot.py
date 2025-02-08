import random

from AIService.base_ai import BaseAI

class MaxPrestigeBot(BaseAI):
    
    def select_patron(self, available_patrons):
        #print(f"MaxPrestigeBot select patron: {available_patrons}")
        return random.choice(available_patrons)
    
    def play(self, game_state, possible_moves):
        #print(f"MaxPrestigeBot play")
        # game_state.debug_print()
        return random.choice(possible_moves)
    
    def game_end(self, final_state):
        pass