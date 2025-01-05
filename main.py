import os
import sys
import subprocess
import threading
import grpc
from concurrent import futures
from Protos import main_pb2_grpc
from Protos import main_pb2
import random
import time

rng = random.Random()

def run_game_runner(arg1, arg2):
    game_runner_path = "GameRunner.exe"
    game_runner_dir = os.path.join(os.getcwd(), "GameRunner")
    
    if not os.path.exists(game_runner_dir):
        print(f"Couldn't find directory {game_runner_dir}")
        return
    
    os.chdir(game_runner_dir)
    
    if not os.path.exists(game_runner_path):
        print(f"Couldn't find file {game_runner_path}")
        return
    
    try:
        subprocess.run([game_runner_path, arg1, arg2], check=True)
        print(f"GameRunner.exe was run with arguments: {arg1}, {arg2}")
    except subprocess.CalledProcessError as e:
        print(f"Couldn't run GameRunner.exe: {e}")


class AIService(main_pb2_grpc.AIServiceServicer):

    def __init__(self, botName):
        self.botName = botName


    def RegisterBot(self, request, context):
        print("Sending register message")
        return main_pb2.RegistrationStatus(name=self.botName, message='Im registering')

    def PregamePrepare(self, request, context):
        print("PregamePrepare called")
        return main_pb2.Empty()

    def SelectPatron(self, request, context):
        return main_pb2.PatronIdMessage(patronId=rng.choice(request.availablePatrons))

    def Play(self, request, context):
        # Return a last move
        print(f'Play: {request.possibleMoves[-1]}')
        return request.possibleMoves[-1]

    def GameEnd(self, request, context):
        print("GameEnd called with:", request)
        return main_pb2.Empty()

    def CloseServer(self, request, context):
        print("Received CloseServer request. Shutting down server...")
        context.set_code(grpc.StatusCode.OK)
        context.set_details("Server will be closed.")
        
        server.stop(0)
        return main_pb2.Empty()

def run_grpc_server():
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    main_pb2_grpc.add_AIServiceServicer_to_server(AIService('Testbot1'), server)
    main_pb2_grpc.add_AIServiceServicer_to_server(AIService('Testbot2'), server)
    server.add_insecure_port("[::]:50000")
    server.add_insecure_port("[::]:50001")
    print("AIService server running on port 50000 and 50001")
    server.start()
    server.wait_for_termination()

def main():
    if len(sys.argv) != 3:
        print("Provide two bot names")
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        
        grpc_thread = threading.Thread(target=run_grpc_server)
        grpc_thread.start()
        time.sleep(1)
        run_game_runner(arg1, arg2)
        
        grpc_thread.join()

if __name__ == "__main__":
    main()