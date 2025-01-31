class BaseAI:
    def __init__(self, bot_name):
        self.bot_name = bot_name

    def pregame_prepare(self):
        pass

    def select_patron(self, available_patrons):
        raise NotImplementedError

    def play(self, game_state, possible_moves):
        raise NotImplementedError

    def game_end(self, final_state):
        pass
