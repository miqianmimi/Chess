turn = fen.split(" ")[1]
if turn == 'b':
    c = b.king(1)
    a = chess.square_name(c)
    if b.is_attacked_by(0, c):
        attackers = b.attackers(0, c)
        for i in attackers:
            t = chess.square_name(i)
            move = str(t) + str(a)
            Move.append(move)
            p = chess.Board(fen)
            p.push(chess.Move.from_uci(str(move)))
            fenn = p.fen()
            Move_value.append(minimax(fenn, current_depth=1, max_depth=4))
            print i
            # 找到将军的棋子
        bbest = Move[0]
        best_move_value = Move_value[0]
        for i in range(len(Move)):
            if Move_value[i] > best_move_value:
                bbest = Move[i]
                best_move_value = Move_value[i]
        print Move
        print Move_value
        return str(bbest)
if turn == 'w':
    c = b.king(0)
    a = chess.square_name(c)
    if b.is_attacked_by(1, c):
        attackers = b.attackers(1, c)
        for i in attackers:
            t = chess.square_name(i)
            move = str(t) + str(a)
            Move.append(move)
            p = chess.Board(fen)
            p.push(chess.Move.from_uci(str(move)))
            fenn = p.fen()
            Move_value.append(minimax(fenn, current_depth=1, max_depth=4))
            print i
            # 找到将军的棋子
        bbest = Move[0]
        best_move_value = Move_value[0]
        for i in range(len(Move)):
            if Move_value[i] > best_move_value:
                bbest = Move[i]
                best_move_value = Move_value[i]
        print Move
        print Move_value
        return str(bbest)
