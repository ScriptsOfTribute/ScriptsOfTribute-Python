from typing import Dict, List, Union

from Protos import basics_pb2, main_pb2
from ScriptsOfTribute.enums import MoveEnum, PatronId, CardType, ChoiceDataType, PlayerEnum, BoardState
from ScriptsOfTribute.board import GameState, UniqueCard, PatronStates, SerializedAgent, Choice, CardOptions, EffectOptions, SeededGameState, CurrentPlayer, EnemyPlayer
from ScriptsOfTribute.move import BasicMove, SimpleCardMove, SimplePatronMove, MakeChoiceMoveUniqueCard, MakeChoiceMoveUniqueEffect



