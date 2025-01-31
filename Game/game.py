from typing import List
from AIService.base_ai import BaseAI
from Game.runner import run_game_runner
from AIService.Server import Server

class Game:
    def __init__(self):
        self.bots: List[BaseAI] = []

    def register_bot(self, bot_instance: BaseAI):
        self.bots.append(bot_instance)

    def run(self, bot1Name: str, bot2Name: str, start_game_runner=True, runs=1, enable_logs="NONE", log_destination="", seed=None, timeout=30):
        server = Server()
        grpc_server = server.run_grpc_server(filter(lambda bot: bot.bot_name == bot1Name or bot.bot_name == bot2Name, self.bots))
        if start_game_runner:
            if any([bot1Name == bot.bot_name for bot in self.bots]):
                bot1Name = "grpc:" + bot1Name
            if any([bot2Name == bot.bot_name for bot in self.bots]):
                bot2Name = "grpc:" + bot2Name
            run_game_runner(
                bot1Name,
                bot2Name, 
                runs=runs, 
                enable_logs=enable_logs,
                log_destination=log_destination,
                seed=seed,
                timeout=timeout
            )
        try:
            grpc_server.wait_for_termination()
        except KeyboardInterrupt:
            print("Server interrupted by user.")
