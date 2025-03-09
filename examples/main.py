from bots.RandomBot import RandomBot
from bots.MaxPrestigeBot import MaxPrestigeBot
from scripts_of_tribute.game import Game


def main():
    bot1 = RandomBot(bot_name="RandomBot")
    bot2 = MaxPrestigeBot(bot_name="MaxPrestigeBot")
    
    game = Game()
    game.register_bot(bot1)
    game.register_bot(bot2)
    
    game.run(
        "RandomBot",
        "MaxPrestigeBot",
        start_game_runner=True,
        runs=5,
        threads=1,
    )

if __name__ == "__main__":
    main()
