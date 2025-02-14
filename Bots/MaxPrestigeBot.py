import random

from AIService.base_ai import BaseAI

class MaxPrestigeBot(BaseAI):
    
    def select_patron(self, available_patrons):
        #print(f"MaxPrestigeBot select patron: {available_patrons}")
        return random.choice(available_patrons)
    
    def play(self, game_state, possible_moves):
        best_move = None
        best_prestige = -1

        for first_move in possible_moves:
            new_game_state, new_moves = game_state.apply_move(first_move)

            for second_move in new_moves:
                final_game_state, _ = new_game_state.apply_move(second_move)

        return random.choice(possible_moves)
    
    def game_end(self, final_state):
        pass