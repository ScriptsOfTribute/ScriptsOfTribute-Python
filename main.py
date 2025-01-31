from Game.game import Game
from AIService.base_ai import BaseAI

class MyBot(BaseAI):
    
    def select_patron(self, available_patrons):
        print("selecting patron")
        return available_patrons[0]
    
    def play(self, game_state, possible_moves):
        return possible_moves[-1]
    
    def game_end(self, final_state):
        pass

def main():
    bot1 = MyBot(bot_name="Bot1")
    bot2 = MyBot(bot_name="Bot2")
    
    game = Game()
    game.register_bot(bot1)
    game.register_bot(bot2)
    
    game.run("Bot1", "RandomBot", start_game_runner=False, runs=5)

if __name__ == "__main__":
    main()
