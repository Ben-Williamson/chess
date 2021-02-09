import webbrowser
import copy

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

def squareToBoardIndex(square):
    return 8-int(square[1]), -1 * (97 - ord(square[0]))

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

    return posibleMoves

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
                        elif(player == "w" and board[i+count][j].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+count, j))
                            blocked = True
                        elif(player == "b" and board[i+count][j].isupper()):
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
                        elif(player == "w" and board[i][j+count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j+count))
                            blocked = True
                        elif(player == "b" and board[i][j+count].isupper()):
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
                        elif(player == "w" and board[i][j-count].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i, j-count))
                            blocked = True
                        elif(player == "b" and board[i][j-count].isupper()):
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
                        elif(player == "w" and board[i-count][j].islower()):
                            posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-count, j))
                            blocked = True
                        elif(player == "b" and board[i-count][j].isupper()):
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

def getKnightMoves(game):
    board = game["board"]
    player = game["toMove"]
    posibleMoves = []

    if(player == "w"):
        target = "N"
    else:
        target = "n"

    for j in range(8):
        for i in range(8):
            if(board[i][j] == target):
                try:
                    currentSquare = board[i+1][j+2]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+1, j+2))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+1, j+2))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+1, j+2))
                except:
                    pass

                try:
                    currentSquare = board[i-1][j+2]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-1, j+2))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-1, j+2))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-1, j+2))
                except:
                    pass

                try:
                    currentSquare = board[i+1][j-2]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+1, j-2))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+1, j-2))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+1, j-2))
                except:
                    pass

                try:
                    currentSquare = board[i-1][j-2]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-1, j-2))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-1, j-2))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-1, j-2))
                except:
                    pass

                try:
                    currentSquare = board[i+2][j+1]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+2, j+1))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+2, j+1))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+2, j+1))
                except:
                    pass

                try:
                    currentSquare = board[i+2][j-1]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+2, j-1))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+2, j-1))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+2, j-1))
                except:
                    pass

                try:
                    currentSquare = board[i-2][j+1]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-2, j+1))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-2, j+1))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-2, j+1))
                except:
                    pass

                try:
                    currentSquare = board[i-2][j-1]
                    if(currentSquare == " "):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-2, j-1))
                    elif(currentSquare.islower() and player == "w"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-2, j-1))
                    elif(currentSquare.isupper() and player == "b"):
                        posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i-2, j-1))
                except:
                    pass

    return posibleMoves

def getKingMoves(game):
    board = game["board"]
    player = game["toMove"]
    posibleMoves = []

    if(player == "w"):
        target = "K"
    else:
        target = "k"

    for j in range(8):
        for i in range(8):
            if(board[i][j] == target):
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if(not (a == 0 and b == 0)):
                            if (i + a > -1) and (i + a) < 8 and (j + b > -1) and (j + b < 8):
                                currentSquare = board[i+a][j+b]
                                if(currentSquare == " "):
                                    posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+a, j+b))
                                elif(currentSquare.islower() and player == "w"):
                                    posibleMoves.append(boardIndexToSquare(i, j) + boardIndexToSquare(i+a, j+b))
    return posibleMoves

def isThisCheck(game):
    out = []

    board = game["board"]
    player = game["toMove"]

    if(player == "w"):
        game["toMove"] = "b"
    else:
        game["toMove"] = "w"

    posibleMoves = []
    posibleMoves.append(getPawnMoves(game))
    posibleMoves.append(getRookMoves(game))
    posibleMoves.append(getKnightMoves(game))
    posibleMoves.append(getBishopMoves(game))
    posibleMoves.append(getQueenMoves(game))
    posibleMoves.append(getKingMoves(game))

    if(game["toMove"] == "w"):
        game["toMove"] = "b"
    else:
        game["toMove"] = "w"

    posibleMoves = [item for sublist in posibleMoves for item in sublist]

    destinationSquares = [item[-2:] for item in posibleMoves]

    if(player == "w"):
        target = "K"
    else:
        target = "k"


    ## CHECK FOR CHECKS

    for j in range(8):
        for i in range(8):
            if(board[i][j] == target):
                if boardIndexToSquare(i, j) in destinationSquares:
                    kingDestinationSquares = [item[-2:] for item in getKingMoves(game)]
                    for square in kingDestinationSquares:
                        if square not in destinationSquares:
                            out.append(square)
                    if(out != []):
                        return 1
                    else:
                        return 2
                else:
                    return 0
    return "ERROR"

def move(game, move):

    localgame = copy.deepcopy(game)

    startSquare = move[:2]
    endSquare = move[-2:]

    piece = localgame["board"][squareToBoardIndex(startSquare)[0]][squareToBoardIndex(startSquare)[1]]
    localgame["board"][squareToBoardIndex(startSquare)[0]][squareToBoardIndex(startSquare)[1]] = " "
    localgame["board"][squareToBoardIndex(endSquare)[0]][squareToBoardIndex(endSquare)[1]] = piece

    return localgame

def findAllMoves(game):
    check = isThisCheck(game)

    if(check == 1 or check == 2):
        return check

    moves = []
    moves.append(getPawnMoves(game))
    moves.append(getRookMoves(game))
    moves.append(getKnightMoves(game))
    moves.append(getBishopMoves(game))
    moves.append(getQueenMoves(game))
    moves.append(getKingMoves(game))

    moves = [item for sublist in moves for item in sublist]

    legalMoves = []

    for Move in moves:
        tempgame = move(game, Move)
        check = isThisCheck(tempgame)
        if(check == 0):
            legalMoves.append(Move)

    return legalMoves

#FEN = "kK6/2R1P1p1/8/3B4/8/r7/8/8 w KQkq e3 0 1"
#FEN = "1r6/1q2bp2/2k5/K7/3r3P/4pp2/1pnn3P/2Q2B2 w - - 0 1"
#FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

FEN = "K7/8/8/B7/8/8/8/1r6 w - - 0 1"

webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open("https://lichess.org/editor/" + FEN)

game = FENtoGame(FEN)

boardPrinter(game)

#move(game, "a8a7")

#boardPrinter(game)

print(findAllMoves(game))

