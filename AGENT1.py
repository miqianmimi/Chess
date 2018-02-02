import chess
def respond_to(fen):
    c=ab_make_move(fen)
    return str(c)


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



'''
board_status= fen
'''
##########来定义启发函数##################
'''
启发函数分为4块：
第一块，启发函数是计算局面上的剩余棋子的和，不同棋子，权重不同
第二块，启发函数是计算局面上所有可走的棋，走后的状态，移动范围大不大，QUEEN在中间有八个，QUEEN边上只有三个
第三块，启发函数是针对小兵的布局是否紧凑
第四块，启发函数判断有没有将军局势产生
'''

def material(fen, weight1):
    points = 0
    piece_values = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 0, 'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 0}
    board_state = fen.split(" ")[0]
    # current_status=board_state.split()[1]
    for piece in board_state:
        if piece.islower():  # w
            points += piece_values[piece]
        elif piece.isupper():
            points -= piece_values[piece]
    return points * weight1

def piece_moves(fen, weight2):
    points = 0
    current_status = fen.split(" ")[1]
    possible_moves = chess.Board(fen).legal_moves
    square_values = {"e4": 1, "e5": 1, "d4": 1, "d5": 1, "c6": 0.5, "d6": 0.5, "e6": 0.5, "f6": 0.5,
                     "c3": 0.5, "d3": 0.5, "e3": 0.5, "f3": 0.5, "c4": 0.5, "c5": 0.5, "f4": 0.5, "f5": 0.5}
    for move in possible_moves:
        if current_status == 'w':
            if str(move)[2:4] in square_values:
                points -= square_values[str(move)[2:4]]
        elif current_status == 'b':
            if str(move)[2:4] in square_values:
                points += square_values[str(move)[2:4]]
    return points * weight2

def pawn_structure(fen, weight3):
    points = 0
    board_state, current_player = [seg for seg in fen.split()[:2]]
    board_state = board_state.split('/')
    board_state_arr = []  # new_fen
    for row in board_state:
        row_arr = []
        for char in row:
            if char.isdigit():
                for i in range(int(char)):
                    row_arr.append(" ")
            else:
                row_arr.append(char)
        board_state_arr.append(row_arr)
    for i, row in enumerate(board_state_arr):
        for j in range(len(row)):
            if board_state_arr[i][j] == "p":
                tl = i - 1, j - 1
                tr = i - 1, j + 1
                if tl[0] >= 0 and tl[0] <= 7 and tl[1] >= 0 and tl[1] <= 7:
                    if board_state_arr[tl[0]][tl[1]] == "p":
                        points += 1
                if tr[0] >= 0 and tr[0] <= 7 and tr[1] >= 0 and tr[1] <= 7:
                    if board_state_arr[tr[0]][tr[1]] == "p":
                        points += 1
    return points * weight3

def checkmate(fen, weight4):
    points = 0
    turn = fen.split(" ")[1]
    current_status = chess.Board(fen).status()
    if turn == "w":
        if current_status == 1:
            points += 1 * weight4
        elif current_status == 2:
            points += float("inf")
    else:
        if current_status == 1:
            points -= 1 * weight4
        elif current_status == 2:
            points += float("-inf")
    return points

def get_heuristic(fen):
    total_points = 0
    # total piece count
    total_points += material(fen, 100)
    total_points += piece_moves(fen, 50)
    total_points += pawn_structure(fen, 1)
    total_points += checkmate(fen, 1)
    return total_points

############来定义搜索算法##################
'''
1.一个minimax 返回启发函数
2.一个abminimax 返回启发函数
3.一个make_move 得到最好的启发函数值的走法，根据minimax
4.一个ab make_move 得到最好的启发函数的值的走法，根据abminimax
'''

def minimax(fen, current_depth, max_depth):
    # b=chess.Board(fen)
    ##   b.push(chess.Move.from_uci(t))
    current_depth += 1
    if current_depth == max_depth:
        fen_value = get_heuristic(fen)
        return fen_value
    elif current_depth % 2 == 0:
        # min player"s turn
        value_min=float("inf")
        for c in list(chess.Board(fen).legal_moves):
            b = chess.Board(fen)
            b.push(chess.Move.from_uci(str(c)))
            fennn=b.fen()
            value=minimax(fennn,current_depth,max_depth)
            if value<value_min:
                value_min=value
        return value_min
    else:
        # max player's turn
        value_max = -float("inf")
        for c in list(chess.Board(fen).legal_moves):
            b = chess.Board(fen)
            b.push(chess.Move.from_uci(str(c)))
            fennn=b.fen()
            value=minimax(fennn,current_depth,max_depth)
            if value>value_max:
                value_max=value
        return value_max



def make_move(fen):
    b = chess.Board(fen)
    possible_move =list(b.legal_moves)
    Move = []
    Move_value = []
    for move in possible_move:
        c=chess.Board(fen)
        Move.append(str(move))
        c.push(chess.Move.from_uci(str(move)))
        fenn=c.fen()
        Move_value.append(minimax(fenn, current_depth=1, max_depth=4))
    Best_move = Move[0]
    best_move_value = Move_value[0]
    for i in range(len(Move)):
        if Move_value[i] > best_move_value:
            Best_move = Move[i]
            best_move_value = Move_value[i]

    print("单纯Minimax")
    #print Move[15]
    #print Move_value[15]
    print Move_value


    return str(Best_move)




'''
1.str(move)
2.fen->epd
'''
def ab_minimax(fen, alpha, beta, current_depth, max_depth):
    current_depth += 1
    if current_depth == max_depth:
        fen_value = get_heuristic(fen)
        if current_depth % 2 == 0:
            if alpha < fen_value:
                alpha = fen_value
            return alpha
        else:
            if beta > fen_value:
                beta = fen_value
            return beta
    if current_depth % 2 == 0:
        # min player"s turn
        for c in chess.Board(fen).legal_moves:
            b = chess.Board(fen)
            b.push(chess.Move.from_uci(str(c)))
            fenn=b.fen()
            if alpha < beta:
                fen_value = ab_minimax(fenn, alpha, beta, current_depth,max_depth)
                if beta > fen_value:
                    beta = fen_value
        return beta
    else:
        # max player"s turn
        for c in chess.Board(fen).legal_moves:
            b = chess.Board(fen)
            b.push(chess.Move.from_uci(str(c)))
            fenn = b.fen()
            if alpha < beta:
                fen_value = ab_minimax(fenn, alpha, beta, current_depth,max_depth)
                #print fen_value
                if alpha < fen_value:
                    alpha = fen_value
        return alpha

def ab_make_move(fen):
    b = chess.Board(fen)
    possible_move = list(b.legal_moves)
    #print len(possible_move)
    Move = []
    Move_value = []
    alpha = float("-inf")
    beta = float("inf")
    for move in possible_move:
        c=chess.Board(fen)
        Move.append(str(move))
        c.push(chess.Move.from_uci(str(move)))
        #print_board(b.board_fen())
        fenn=c.fen()
        #print Move
        #print_board(c.board_fen())
        #print fenn
        board_value = ab_minimax(fenn, alpha, beta, 1, 4)
        Move_value.append(board_value)
        if alpha < board_value:
            alpha = board_value
            Best_move = move
            Best_move_value = alpha
    print("ab+Minimax")
    print Move_value
    #print Move_value[15]
    #print Move[15]

    #print Move_value
    #print len(Move_value)
    #print len(Move)
    return str(Best_move)
