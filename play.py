import chess
import AGENT as agent
import AGENT1 as agent_smart
'''
black on the top
white on the low
'''

###############FOR_BEAUTIFUL SHOWING#####################

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



###############MAIN_FUNCTION#####################
'''
对比random AI ；
1.random AI 
2. AB minimax AI 
3. minimax AI
2.3结果一样，但2更快

'''
#pp = []
d=agent_smart.make_move("rnbqkbnr/pp1ppppp/4K3/2p5/4P3/8/PPPP1PPP/RNBQ1BNR b KQkq c6 0 2")
c=agent_smart.ab_make_move("rnbqkbnr/pp1ppppp/4K3/2p5/4P3/8/PPPP1PPP/RNBQ1BNR b KQkq c6 0 2")
#pp.append(agent_smart.minimax('rnbqkbnr/pp1ppppp/8/2p1P3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2', current_depth=1, max_depth=5))
#print pp

#a=agent.respond_to("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")

#board = chess.Board("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
#print_board(board.board_fen())
#board.push(chess.Move.from_uci(a))
#print a
#print_board(board.board_fen())


print ('minimax')
board = chess.Board("rnbqkbnr/pp1ppppp/4K3/2p5/4P3/8/PPPP1PPP/RNBQ1BNR b KQkq c6 0 2")
board.push(chess.Move.from_uci(d))
print d
print board
print_board(board.board_fen())


print ('ab_minimax')
board = chess.Board("rnbqkbnr/pp1ppppp/4K3/2p5/4P3/8/PPPP1PPP/RNBQ1BNR b KQkq c6 0 2")
board.push(chess.Move.from_uci(c))
print c
print_board(board.board_fen())


#print_board(b.board_fen())


#for c in b.legal_moves:
    #print (c)
#print(b.piece_at(chess.C8))
#print_board(b.board_fen())
#fen=str("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#a=get_heuristic(fen)
#print a
#fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
#fen = fen.split()[0].split("/")
#print(fen)