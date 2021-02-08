import webbrowser

def FENtoGame(FEN):
    board = [[" " for i in range(8)] for i in range(8)]

    pieces = FEN.split(" ")[0].split("/")

    pieceIndex = 0
    while pieceIndex < len(pieces):
        rank = pieces[pieceIndex]
        rankIndex = 0
        file = 0
        while rankIndex < len(rank):
            try:
                file += int(rank[rankIndex])
            except:
                board[pieceIndex][file] = rank[rankIndex]
                file += 1
            rankIndex += 1
        pieceIndex += 1

    game = {
        "board": board,
        "toMove": FEN.split(" ")[1],
        "castle": FEN.split(" ")[2],
        "enPassant": FEN.split(" ")[3],
    }
    return game

def boardPrinter(game):
    board = game["board"]
    print("+------------------+")
    for rank in board:
        out = "| "
        for piece in rank:
            out += piece + " "
        out += " |"
        print(out)
    print("+------------------+")

def boardIndexToSquare(y, x):
    return chr(97+x) + str(8-y)

def getPawnMoves(game):
    board = game["board"]
    player = game["toMove"]
    posibleMoves = []

    if(player == "w"):
        target = "P"
        direction = -1
        secondRank = 6
    else:
        target = "p"
        direction = +1
        secondRank = 1

    for j in range(8):
        for i in range(8):
            if(board[i][j] == target):  # Is there a pawn here?
                if(board[i + direction][j] == " "):  # Is the space infront free?
                    if((player == "w") and (i == 1)):
                        promotePieces = ["q", "r", "n", "b"]
                        for piece in promotePieces:
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction, j) + piece)
                    elif((player == "b") and (i == 6)):
                        promotePieces = ["q", "r", "n", "b"]
                        for piece in promotePieces:
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction, j) + piece)
                    else:
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction, j))

                if((i == secondRank) and (board[i + direction][j] == " ") and (board[i + direction * 2][j] == " ")):  # Is the pawn on the second rank and are the two spaces infront free?
                    posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction * 2, j))
                
                if(j < 7):
                    left = board[i + direction][j+1]
                    if((left != " ") and (player == "w") and (left.islower())):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction, j + 1))
                    if((left != " ") and (player == "b") and (left.isupper())):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction, j + 1))
                if(j > 0):
                    right = board[i + direction][j-1]
                    if((right != " ") and (player == "w") and (right.islower())):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction, j - 1))
                    if((right != " ") and (player == "b") and (right.isupper())):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i + direction, j - 1))

    print(posibleMoves)

def getRookMoves(game):
    board = game["board"]
    player = game["toMove"]
    posibleMoves = []

    if(player == "w"):
        target = "R"
    else:
        target = "r"

    for j in range(8):
        for i in range(8):
            if(board[i][j] == target):
                blocked = False
                count = 1
                while not blocked:
                    if(i + count == 8):
                        blocked = True
                    else:
                        if(board[i+count][j] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j))
                        elif(board[i+count][j].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if(j + count == 8):
                        blocked = True
                    else:
                        if(board[i][j+count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j+count))
                        elif(board[i][j+count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j+count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if(j - count + 1 == 0):
                        blocked = True
                    else:
                        if(board[i][j-count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j-count))
                        elif(board[i][j-count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j-count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if(i - count + 1 == 0):
                        blocked = True
                    else:
                        if(board[i-count][j] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j))
                        elif(board[i-count][j].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j))
                            blocked = True
                        else:
                            blocked = True
                        count += 1
    return posibleMoves

def getBishopMoves(game):
    board = game["board"]
    player = game["toMove"]
    posibleMoves = []

    if(player == "w"):
        target = "B"
    else:
        target = "b"

    for j in range(8):
        for i in range(8):
            if(board[i][j] == target):
                blocked = False
                count = 1
                while not blocked:
                    if((i + count == 8) or (j+count == 8)):
                        blocked = True
                    else:
                        if(board[i+count][j+count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j+count))
                        elif(board[i+count][j+count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j+count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if((i - count + 1 == 0) or (j+count == 8)):
                        blocked = True
                    else:
                        if(board[i-count][j+count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j+count))
                        elif(board[i-count][j+count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j+count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if((i + count == 8) or (j - count + 1 == 0)):
                        blocked = True
                    else:
                        if(board[i+count][j-count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j-count))
                        elif(board[i+count][j-count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j-count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if((i - count + 1 == 0) or (j - count + 1 == 0)):
                        blocked = True
                    else:
                        if(board[i-count][j-count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j-count))
                        elif(board[i-count][j-count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j-count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

    return posibleMoves

def getQueenMoves(game):
    board = game["board"]
    player = game["toMove"]
    posibleMoves = []

    if(player == "w"):
        target = "Q"
    else:
        target = "q"

    for j in range(8):
        for i in range(8):
            if(board[i][j] == target):
                blocked = False
                count = 1
                while not blocked:
                    if((i + count == 8) or (j+count == 8)):
                        blocked = True
                    else:
                        if(board[i+count][j+count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j+count))
                        elif(board[i+count][j+count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j+count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if((i - count + 1 == 0) or (j+count == 8)):
                        blocked = True
                    else:
                        if(board[i-count][j+count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j+count))
                        elif(board[i-count][j+count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j+count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if((i + count == 8) or (j - count + 1 == 0)):
                        blocked = True
                    else:
                        if(board[i+count][j-count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j-count))
                        elif(board[i+count][j-count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j-count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if((i - count + 1 == 0) or (j - count + 1 == 0)):
                        blocked = True
                    else:
                        if(board[i-count][j-count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j-count))
                        elif(board[i-count][j-count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j-count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if(i + count == 8):
                        blocked = True
                    else:
                        if(board[i+count][j] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j))
                        elif(board[i+count][j].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if(j + count == 8):
                        blocked = True
                    else:
                        if(board[i][j+count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j+count))
                        elif(board[i][j+count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j+count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if(j - count + 1 == 0):
                        blocked = True
                    else:
                        if(board[i][j-count] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j-count))
                        elif(board[i][j-count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j-count))
                            blocked = True
                        else:
                            blocked = True
                        count += 1

                blocked = False
                count = 1
                while not blocked:
                    if(i - count + 1 == 0):
                        blocked = True
                    else:
                        if(board[i-count][j] == " "):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j))
                        elif(board[i-count][j].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j))
                            blocked = True
                        else:
                            blocked = True
                        count += 1
    return posibleMoves

#FEN = "kK6/2R1P1p1/8/3B4/8/r7/8/8 w KQkq e3 0 1"
#FEN = "1r6/1q2bp2/2k5/K7/3r3P/4pp2/1pnn3P/2Q2B2 w - - 0 1"
#FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

FEN = "8/8/8/2P1p3/3Q4/2P14/8/8 w - - 0 1"

webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open("https://lichess.org/editor/" + FEN)

game = FENtoGame(FEN)

boardPrinter(game)

print(getQueenMoves(game))

