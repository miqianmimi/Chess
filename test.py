import chess
import sys
import time
import AGENT1 as agentWhite
import agentrjw as agentBlack
#import agentLM as agentBlack
#import agent_version8 as agentBlack

global count
count = 0
def print_board(board_state, captured={"w": [], "b": []}):
    PIECE_SYMBOLS = {'P': '♟',
                     'B': '♝',
                     'N': '♞',
                     'R': '♜',
                     'Q': '♛',
                     'K': '♚',
                     'p': '\033[36m\033[1m♙\033[0m',
                     'b': '\033[36m\033[1m♗\033[0m',
                     'n': '\033[36m\033[1m♘\033[0m',
                     'r': '\033[36m\033[1m♖\033[0m',
                     'q': '\033[36m\033[1m♕\033[0m',
                     'k': '\033[36m\033[1m♔\033[0m'}
    board_state = board_state.split()[0].split("/")
    board_state_str = "\n"
    white_captured = " ".join(PIECE_SYMBOLS[piece] for piece in captured['w'])
    black_captured = " ".join(PIECE_SYMBOLS[piece] for piece in captured['b'])
    for i, row in enumerate(board_state):
        board_state_str += str(8 - i)
        for char in row:
            if char.isdigit():
                board_state_str += " ♢" * int(char)
            else:
                board_state_str += " " + PIECE_SYMBOLS[char]
        if i == 0:
            board_state_str += "   Captured:" if len(white_captured) > 0 else ""
        if i == 1:
            board_state_str += "   " + white_captured
        if i == 6:
            board_state_str += "   Captured:" if len(black_captured) > 0 else ""
        if i == 7:
            board_state_str += "   " + black_captured
        board_state_str += "\n"
    board_state_str += "  A B C D E F G H"
    print(board_state_str)


def game_start():
    board = chess.Board()
    while not board.is_game_over():
        start = time.clock()
        if(board.turn == chess.WHITE):
            move = agentWhite.respond_to(board.fen())
        else:
            move = agentBlack.respond_to(board.fen())
        end = time.clock()

        board.push(chess.Move.from_uci(move))
        global count
        count += 1
        print_board(board.fen())
        print 'Steps:\t\t\t' , count
        print 'Time consumption: \t' , (end - start) , 's'
    print('END')
    print(board.result(claim_draw=False))

game_start()
