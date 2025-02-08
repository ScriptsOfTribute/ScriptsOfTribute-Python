from threading import Lock
from typing import List
import grpc
from concurrent import futures

from Protos import main_pb2_grpc, main_pb2
from AIService.base_ai import BaseAI
from ScriptsOfTribute.board import build_game_state
from ScriptsOfTribute.move import from_proto_move
from ScriptsOfTribute.enums import PatronId

class AIService(main_pb2_grpc.AIServiceServicer):
    def __init__(self, ai: BaseAI, server_instance):
        self.ai = ai
        self.server_instance = server_instance
        self.engine_service_stub = None

    def set_engine_service_stub(self, stub):
        self.engine_service_stub = stub

    def RegisterBot(self, request, context):
        return main_pb2.RegistrationStatus(name=self.ai.bot_name, message="")

    def PregamePrepare(self, request, context):
        self.ai.pregame_prepare()
        return main_pb2.Empty()

    def SelectPatron(self, request, context):
        patrons = [PatronId(patron) for patron in request.availablePatrons]
        patron = self.ai.select_patron(patrons)
        return main_pb2.PatronIdMessage(patronId=patron.value)

    def Play(self, request, context):
        game_state = build_game_state(request.gameState, self.engine_service_stub)
        # game_state.debug_print()
        moves = [from_proto_move(proto_move) for proto_move in request.possibleMoves]
        move = self.ai.play(game_state, moves)
        return move.to_proto()

    def GameEnd(self, request, context):
        self.ai.game_end(request)
        return main_pb2.Empty()

    def CloseServer(self, request, context):
        print("Received CloseServer request. Shutting down server...")
        self.server_instance.bot_disconnected()
        context.set_code(grpc.StatusCode.OK)
        context.set_details(f"Bot {self.ai.bot_name}'s connection closed.")
        return main_pb2.Empty()
    

class Server:

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.active_bots = 0
                cls._instance.server = None
                cls._instance.lock = Lock()
        return cls._instance

    def add_bot(self):
        with self.lock:
            self.active_bots += 1
            print(f"Bot connected. Active bots: {self.active_bots}")

    def bot_disconnected(self):
        with self.lock:
            self.active_bots -= 1
            print(f"Bot disconnected. Active bots: {self.active_bots}")
            if self.active_bots == 0:
                self.shutdown_server()

    def shutdown_server(self):
        if self.server:
            print("No active bots. Shutting down the server...")
            self.server.stop(0)
        else:
            print("Server is already stopped.")

    def run_grpc_server(self, ai_instances: List[BaseAI], port=50000, debug_prints=True):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        for i, ai in enumerate(ai_instances):
            self.add_bot()
            ai_service = AIService(ai, self)
            assigned_port = port + i
            self.server.add_insecure_port(f"localhost:{assigned_port}")
            engine_service_channel = grpc.insecure_channel(f"localhost:{assigned_port}")
            engine_service_stub = main_pb2_grpc.EngineServiceStub(engine_service_channel)
            if debug_prints:
                print(f"Bot {ai.bot_name} listening on localhost:{assigned_port}")
            ai_service.set_engine_service_stub(engine_service_stub)

            main_pb2_grpc.add_AIServiceServicer_to_server(ai_service, self.server)
        self.server.start()
        return self.server
