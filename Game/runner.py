import os
import subprocess

def run_game_runner(bot1: str, bot2: str, runs=1, threads=1, enable_logs="NONE", log_destination="", seed=None, timeout=30):
    game_runner_path = "GameRunner.exe"
    game_runner_dir = os.path.join(os.getcwd(), "GameRunner")
    
    if not os.path.exists(game_runner_dir):
        raise FileNotFoundError(f"Couldn't find directory {game_runner_dir}")
    
    os.chdir(game_runner_dir)
    
    if not os.path.exists(game_runner_path):
        raise FileNotFoundError(f"Couldn't find file {game_runner_path}")
    
    args = [game_runner_path, bot1, bot2]
    args += ["-n", str(runs)]
    args += ["-t", str(threads)]
    args += ["-l", enable_logs]
    if log_destination:
        args += ["-d", log_destination]
    if seed:
        args += ["-s", str(seed)]
    args += ["-to", str(timeout)]
    print(f'Running: {args}')
    try:
        result = subprocess.run(
            args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running GameRunner.exe:\n{e.stderr}")
        raise RuntimeError(e)

