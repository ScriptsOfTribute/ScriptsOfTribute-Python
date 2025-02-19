import random
from typing import Dict, List, Union

from Protos import basics_pb2, main_pb2
from Protos.main_pb2_grpc import EngineServiceStub
from Protos.main_pb2 import ApplyMoveRequest, SimulationResult, StateId
from ScriptsOfTribute.enums import BoardState, CardType, ChoiceDataType, PatronId, PlayerEnum
from ScriptsOfTribute.move import BasicMove, from_proto_move

class PatronStates:
    def __init__(self, patrons: Dict[PatronId, PlayerEnum]):
        self.patrons = patrons

class UniqueCard:
    def __init__(self, name: str, deck: PatronId, cost: int, type: CardType, hp: int, taunt: bool, unique_id: int, effects: List[str]):
        self.name = name
        self.deck = deck
        self.cost = cost
        self.type = type
        self.hp = hp
        self.taunt = taunt
        self.unique_id = unique_id
        self.effects = effects

class SerializedAgent:
    def __init__(self, currentHP: int, representing_card: UniqueCard, activated: bool):
        self.currentHP = currentHP
        self.representing_card = representing_card
        self.activated = activated

class EndGameState:
    def __init__(self, winner: str, reason: str, AdditionalContext: str):
        self.winner = winner
        self.reason = reason
        self.AdditionalContext = AdditionalContext

class Choice:
    def __init__(
            self,
            max_choices: int,
            min_choices: int, 
            context: str, 
            choice_follow_up: str, 
            type: ChoiceDataType, 
            possible_options: Union['CardOptions', 'EffectOptions']
        ):
        self.max_choices = max_choices
        self.min_choices = min_choices
        self.context = context
        self.choice_follow_up = choice_follow_up
        self.type = type
        self.possible_options = possible_options

class CardOptions:
    def __init__(self, possible_cards: List[UniqueCard]):
        self.possible_cards = possible_cards

class EffectOptions:
    def __init__(self, possible_effects: List[str]):
        self.possible_effects = possible_effects

class CurrentPlayer:
    def __init__(
            self, 
            player_id: PlayerEnum,
            hand: List[UniqueCard],
            cooldown_pile: List[UniqueCard],
            played: List[UniqueCard],
            known_upcoming_draws: List[UniqueCard],
            agents: List['SerializedAgent'],
            power: int,
            patron_calls: int,
            coins: int,
            prestige: int,
            draw_pile: List[UniqueCard]
        ):
        self.player_id = player_id
        self.hand = hand
        self.cooldown_pile = cooldown_pile
        self.played = played
        self.known_upcoming_draws = known_upcoming_draws
        self.agents = agents
        self.power = power
        self.patron_calls = patron_calls
        self.coins = coins
        self.prestige = prestige
        self.draw_pile = draw_pile

class EnemyPlayer:
    def __init__(
            self,
            player_id: PlayerEnum,
            agents: List[SerializedAgent],
            power: int,
            coins: int,
            prestige: int,
            hand_and_draw: List[UniqueCard],
            played: List[UniqueCard],
            cooldown_pile: List[UniqueCard]
        ):
        self.player_id = player_id
        self.agents = agents
        self.power = power
        self.coins = coins
        self.prestige = prestige
        self.hand_and_draw = hand_and_draw
        self.played = played
        self.cooldown_pile = cooldown_pile

class GameState:
    def __init__(
            self,
            state_id: str, 
            patron_states: PatronStates,
            tavern_available_cards: List[UniqueCard],
            board_state: BoardState,
            upcoming_effects: List[str],
            start_of_next_turn_effects: List[str],
            current_player: CurrentPlayer,
            enemy_player: EnemyPlayer,
            completed_actions: List[str],
            tavern_cards: List[UniqueCard],
            pending_choice: Choice | None,
            end_game_state: EndGameState,
            engine_service_stub: EngineServiceStub
        ):
        self.state_id = state_id
        self.patron_states = patron_states
        self.tavern_available_cards = tavern_available_cards
        self.board_state = board_state
        self.upcoming_effects = upcoming_effects
        self.start_of_next_turn_effects = start_of_next_turn_effects
        self.current_player = current_player
        self.enemy_player = enemy_player
        self.completed_actions = completed_actions
        self.tavern_cards = tavern_cards
        self.pending_choice = pending_choice
        self.end_game_state = end_game_state

        self._engine_service_stub = engine_service_stub

    def apply_move(self, move: BasicMove, seed: int=None) -> tuple['SeededGameState', List[BasicMove]]:
        proto_move = move.to_proto()

        if seed is None:
            seed = int(random.random() * 1e18)

        request = ApplyMoveRequest(
            state_id=self.state_id,
            move=proto_move,
            seed=seed
        )

        response: SimulationResult = self._engine_service_stub.ApplyMove(request)

        updated_game_state = build_seeded_game_state(response.gameState, self._engine_service_stub)
        possible_moves = [from_proto_move(move_proto) for move_proto in response.possibleMoves]

        return updated_game_state, possible_moves

    def debug_print(self, indent: int = 0) -> None:
        """
        Print a nicely formatted representation of the GameState for debugging.

        Args:
            indent: The number of spaces to indent nested structures.
        """
        indent_str = " " * indent

        print(f"{indent_str}GameState:")
        print(f"{indent_str}  state_id: {self.state_id}")
        print(f"{indent_str}  patron_states:")
        for patron, player in self.patron_states.patrons.items():
            print(f"{indent_str}    {patron}: {player}")
        print(f"{indent_str}  tavern_available_cards:")
        for card in self.tavern_available_cards:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  board_state: {self.board_state}")
        print(f"{indent_str}  upcoming_effects: {self.upcoming_effects}")
        print(f"{indent_str}  start_of_next_turn_effects: {self.start_of_next_turn_effects}")
        print(f"{indent_str}  current_player:")
        self._print_current_player(self.current_player, indent + 4)
        print(f"{indent_str}  enemy_player:")
        self._print_enemy_player(self.enemy_player, indent + 4)
        print(f"{indent_str}  completed_actions: {self.completed_actions}")
        print(f"{indent_str}  tavern_cards:")
        for card in self.tavern_cards:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  pending_choice:")
        self._print_choice(self.pending_choice, indent + 4)

    def _print_unique_card(self, card: UniqueCard, indent: int) -> None:
        indent_str = " " * indent
        print(f"{indent_str}UniqueCard:")
        print(f"{indent_str}  name: {card.name}")
        print(f"{indent_str}  deck: {card.deck}")
        print(f"{indent_str}  cost: {card.cost}")
        print(f"{indent_str}  type: {card.type}")
        print(f"{indent_str}  hp: {card.hp}")
        print(f"{indent_str}  taunt: {card.taunt}")
        print(f"{indent_str}  unique_id: {card.unique_id}")
        print(f"{indent_str}  effects: {card.effects}")

    def _print_current_player(self, player: CurrentPlayer, indent: int) -> None:
        indent_str = " " * indent
        print(f"{indent_str}CurrentPlayer:")
        print(f"{indent_str}  player_id: {player.player_id}")
        print(f"{indent_str}  hand:")
        for card in player.hand:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  cooldown_pile:")
        for card in player.cooldown_pile:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  played:")
        for card in player.played:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  known_upcoming_draws:")
        for card in player.known_upcoming_draws:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  agents:")
        for agent in player.agents:
            self._print_serialized_agent(agent, indent + 4)
        print(f"{indent_str}  power: {player.power}")
        print(f"{indent_str}  patron_calls: {player.patron_calls}")
        print(f"{indent_str}  coins: {player.coins}")
        print(f"{indent_str}  prestige: {player.prestige}")
        print(f"{indent_str}  draw_pile:")
        for card in player.draw_pile:
            self._print_unique_card(card, indent + 4)

    def _print_enemy_player(self, player: EnemyPlayer, indent: int) -> None:
        indent_str = " " * indent
        print(f"{indent_str}EnemyPlayer:")
        print(f"{indent_str}  player_id: {player.player_id}")
        print(f"{indent_str}  agents:")
        for agent in player.agents:
            self._print_serialized_agent(agent, indent + 4)
        print(f"{indent_str}  power: {player.power}")
        print(f"{indent_str}  coins: {player.coins}")
        print(f"{indent_str}  prestige: {player.prestige}")
        print(f"{indent_str}  hand_and_draw:")
        for card in player.hand_and_draw:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  played:")
        for card in player.played:
            self._print_unique_card(card, indent + 4)
        print(f"{indent_str}  cooldown_pile:")
        for card in player.cooldown_pile:
            self._print_unique_card(card, indent + 4)

    def _print_serialized_agent(self, agent: SerializedAgent, indent: int) -> None:
        indent_str = " " * indent
        print(f"{indent_str}SerializedAgent:")
        print(f"{indent_str}  currentHP: {agent.currentHP}")
        print(f"{indent_str}  representing_card:")
        self._print_unique_card(agent.representing_card, indent + 4)
        print(f"{indent_str}  activated: {agent.activated}")

    def _print_choice(self, choice: Choice, indent: int) -> None:
        if not choice:
            return
        indent_str = " " * indent
        print(f"{indent_str}Choice:")
        print(f"{indent_str}  max_choices: {choice.max_choices}")
        print(f"{indent_str}  min_choices: {choice.min_choices}")
        print(f"{indent_str}  context: {choice.context}")
        print(f"{indent_str}  choice_follow_up: {choice.choice_follow_up}")
        print(f"{indent_str}  type: {choice.type}")
        print(f"{indent_str}  possible_options:")
        if isinstance(choice.possible_options, CardOptions):
            print(f"{indent_str}    CardOptions:")
            for card in choice.possible_options.possible_cards:
                self._print_unique_card(card, indent + 6)
        elif isinstance(choice.possible_options, EffectOptions):
            print(f"{indent_str}    EffectOptions:")
            for effect in choice.possible_options.possible_effects:
                print(f"{indent_str}      {effect}")

class SeededGameState(GameState):
    def __init__(
            self, 
            state_id: str,
            patron_states: PatronStates,
            tavern_available_cards: List[UniqueCard],
            board_state: BoardState,
            upcoming_effects: List[str],
            start_of_next_turn_effects: List[str],
            current_player: CurrentPlayer,
            enemy_player: EnemyPlayer, 
            completed_actions: List[str],
            tavern_cards: List[UniqueCard],
            pending_choice: Choice,
            end_game_state: EndGameState,
            InitialSeed: int,
            CurrentSeed: int,
            engine_service_stub: EngineServiceStub,
        ):
        super().__init__(
            state_id,
            patron_states,
            tavern_available_cards,
            board_state,
            upcoming_effects,
            start_of_next_turn_effects,
            current_player,
            enemy_player,
            completed_actions,
            tavern_cards,
            pending_choice,
            end_game_state,
            engine_service_stub
        )
        self.InitialSeed = InitialSeed
        self.CurrentSeed = CurrentSeed


def build_game_state(proto: main_pb2.GameStateProto, engine_service_stub, seeded=False) -> GameState:
    def convert_unique_card(card_proto: basics_pb2.UniqueCardProto) -> UniqueCard:
        return UniqueCard(
            name=card_proto.name,
            deck=PatronId(card_proto.deck),
            cost=card_proto.cost,
            type=CardType(card_proto.type),
            hp=card_proto.hp,
            taunt=card_proto.taunt,
            unique_id=card_proto.unique_id,
            effects=list(card_proto.effects)
        )

    def convert_serialized_agent(agent_proto: basics_pb2.SerializedAgentProto) -> SerializedAgent:
        return SerializedAgent(
            currentHP=agent_proto.currentHP,
            representing_card=convert_unique_card(agent_proto.representing_card),
            activated=agent_proto.activated
        )

    def convert_patron_states(patron_states_proto: basics_pb2.PatronStatesProto) -> PatronStates:
        patrons = {
            PatronId.from_string(k): PlayerEnum.from_string(v) for k, v in patron_states_proto.patrons.items()
        }
        return PatronStates(patrons=patrons)

    def convert_choice(choice_proto: basics_pb2.ChoiceProto) -> Choice | None:
        if choice_proto == basics_pb2.ChoiceProto():
            return None
        if choice_proto.HasField("card_options"):
            possible_options = CardOptions(
                possible_cards=[convert_unique_card(card) for card in choice_proto.card_options.possible_cards]
            )
        elif choice_proto.HasField("effect_options"):
            possible_options = EffectOptions(
                possible_effects=list(choice_proto.effect_options.possible_effects)
            )
        else:
            raise ValueError("ChoiceProto has no valid possible_options")

        return Choice(
            max_choices=choice_proto.max_choices,
            min_choices=choice_proto.min_choices,
            context=choice_proto.context,
            choice_follow_up=choice_proto.choice_follow_up,
            type=ChoiceDataType(choice_proto.type),
            possible_options=possible_options
        )

    def convert_player(player_proto: basics_pb2.PlayerProto) -> CurrentPlayer:
        return CurrentPlayer(
            player_id=PlayerEnum(player_proto.player_id),
            hand=[convert_unique_card(card) for card in player_proto.hand],
            cooldown_pile=[convert_unique_card(card) for card in player_proto.cooldown_pile],
            played=[convert_unique_card(card) for card in player_proto.played],
            known_upcoming_draws=[convert_unique_card(card) for card in player_proto.known_upcoming_draws],
            agents=[convert_serialized_agent(agent) for agent in player_proto.agents],
            power=player_proto.power,
            patron_calls=player_proto.patron_calls,
            coins=player_proto.coins,
            prestige=player_proto.prestige,
            draw_pile=[convert_unique_card(card) for card in player_proto.draw_pile]
        )

    def convert_enemy_player(enemy_proto: basics_pb2.EnemyPlayerProto) -> EnemyPlayer:
        return EnemyPlayer(
            player_id=PlayerEnum(enemy_proto.player_id),
            agents=[convert_serialized_agent(agent) for agent in enemy_proto.agents],
            power=enemy_proto.power,
            coins=enemy_proto.coins,
            prestige=enemy_proto.prestige,
            hand_and_draw=[convert_unique_card(card) for card in enemy_proto.hand_and_draw],
            played=[convert_unique_card(card) for card in enemy_proto.played],
            cooldown_pile=[convert_unique_card(card) for card in enemy_proto.cooldown_pile]
        )
    
    def convert_end_game_state(end_game_state: basics_pb2.EndGameState) -> EndGameState:
        if end_game_state == basics_pb2.EndGameState():
            return None
        return EndGameState(end_game_state.winner, end_game_state.reason, end_game_state.AdditionalContext)

    return GameState(
        state_id=proto.state_id,
        patron_states=convert_patron_states(proto.patron_states),
        tavern_available_cards=[convert_unique_card(card) for card in proto.tavern_available_cards],
        board_state=BoardState(proto.board_state),
        upcoming_effects=list(proto.upcoming_effects),
        start_of_next_turn_effects=list(proto.start_of_next_turn_effects),
        current_player=convert_player(proto.current_player),
        enemy_player=convert_enemy_player(proto.enemy_player) if not seeded else convert_player(proto.enemy_player),
        completed_actions=list(proto.completed_actions),
        tavern_cards=[convert_unique_card(card) for card in proto.tavern_cards],
        pending_choice=convert_choice(proto.pending_choice),
        end_game_state=convert_end_game_state(proto.end_game_state),
        engine_service_stub=engine_service_stub
    )

def build_seeded_game_state(proto: main_pb2.SeededGameStateProto, engine_service_stub) -> SeededGameState:
    base_game_state = build_game_state(proto, engine_service_stub, seeded=True)
    return SeededGameState(
        state_id=proto.state_id,
        patron_states=base_game_state.patron_states,
        tavern_available_cards=base_game_state.tavern_available_cards,
        board_state=base_game_state.board_state,
        upcoming_effects=base_game_state.upcoming_effects,
        start_of_next_turn_effects=base_game_state.start_of_next_turn_effects,
        current_player=base_game_state.current_player,
        enemy_player=base_game_state.enemy_player,
        completed_actions=base_game_state.completed_actions,
        tavern_cards=base_game_state.tavern_cards,
        pending_choice=base_game_state.pending_choice,
        end_game_state=base_game_state.end_game_state,
        InitialSeed=proto.InitialSeed,
        CurrentSeed=proto.CurrentSeed,
        engine_service_stub=engine_service_stub
    )