from typing import Tuple
import grpc
from concurrent import futures

from Protos import main_pb2_grpc, main_pb2
from AIService.base_ai import BaseAI
from ScriptsOfTribute.board import build_game_state
from ScriptsOfTribute.move import from_proto_move
from ScriptsOfTribute.enums import PatronId

class AIService(main_pb2_grpc.AIServiceServicer):
    def __init__(self, ai: BaseAI, server_instance, engine_service_port:int):
        self.ai = ai
        self.server_instance = server_instance
        self.engine_service_port = engine_service_port
        self.engine_service_stub = None

    def RegisterBot(self, request, context):
        engine_service_channel1 = grpc.insecure_channel(f"localhost:{self.engine_service_port}")
        self.engine_service_stub = main_pb2_grpc.EngineServiceStub(engine_service_channel1)
        print(f"Registering {self.ai.bot_name}")
        print(f"localhost:{self.engine_service_port}")
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
        #game_state.debug_print()
        moves = [from_proto_move(proto_move) for proto_move in request.possibleMoves]
        move = self.ai.play(game_state, moves, request.remainingTimeMs).to_proto()
        # print(move)
        return move

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

    def __init__(self):
        self.active_bots = 0
        self.server = None
    def add_bot(self):
        self.active_bots += 1
        #print(f"Bot connected. Active bots: {self.active_bots}")

    def bot_disconnected(self):
        self.active_bots -= 1
        #print(f"Bot disconnected. Active bots: {self.active_bots}")
        if self.active_bots == 0:
            self.shutdown_server()

    def shutdown_server(self):
        if self.server:
            #print("No active bots. Shutting down the server...")
            self.server.stop(0)
        else:
            print("Server is already stopped.")

def run_grpc_server(
        bot1: BaseAI | None,
        bot2: BaseAI | None,
        base_client_ports: Tuple[int, int]=(50000, 50001),
        base_server_ports: Tuple[int, int]=(49000, 49001),
        debug_prints=True
    ):
    if bot1 is not None:
        server1 = Server()
        server1.server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        server1.add_bot()
        ai_service1 = AIService(bot1, server1, base_server_ports[0])
        server1.server.add_insecure_port(f"localhost:{base_client_ports[0]}")
        main_pb2_grpc.add_AIServiceServicer_to_server(ai_service1, server1.server)
        if debug_prints:
            print(f"Bot {bot1.bot_name} listening on localhost:{base_client_ports[0]}, channel for engine service open on: {base_server_ports[0]}")
        server1.server.start()

    if bot2 is not None:
        server2 = Server()
        server2.server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        server2.add_bot()
        ai_service2 = AIService(bot2, server2, base_server_ports[1])
        server2.server.add_insecure_port(f"localhost:{base_client_ports[1]}")
        main_pb2_grpc.add_AIServiceServicer_to_server(ai_service2, server2.server)
        if debug_prints:
            print(f"Bot {bot2.bot_name} listening on localhost:{base_client_ports[1]}, channel for engine service open on: {base_server_ports[1]}")
        server2.server.start()

    if bot1 is not None:
        server1.server.wait_for_termination()
    if bot2 is not None:
        server2.server.wait_for_termination()
