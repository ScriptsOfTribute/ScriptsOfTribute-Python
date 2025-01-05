import json
import sys
import random

END_OF_TRANSMISSION = "EOT"

def get_game_state():
    data = ''
    while (data_fraction := input()) != END_OF_TRANSMISSION:
        data += data_fraction
    if data.startswith("FINISHED"):
        # Game is over
        _, winner, reason, context = data.split(' ', 3)
        return (winner, reason, context), True
    return json.loads(data), False

def get_patrons_to_pick():
    data = input()
    patrons, round_nr = data.split()
    patrons = patrons.split(',')

    return patrons, round_nr

def debug(msg):
    print(msg, file=sys.stderr)

if __name__ == '__main__':
    debug("Start in python")
    for _ in range(2):
        patrons, round_nr = get_patrons_to_pick()
        debug(f'Received: {patrons} in round {round_nr}')
        print(random.choice(patrons))

    debug("END OF PATRON SELECTION PHASE")
    debug("GAME STARTS")
    while True:
        data, finished = get_game_state()
        if finished:
            debug(data)
            break
        debug(f'Received: {data} of type {type(data)}')
        import pdb; pdb.set_trace()
        print('ENDTURN')
