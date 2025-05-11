#python chess is the library used to simulate legal moves and import fen notation
import chess
#graphical game library
import pygame

import random

scale_factor = 0.75

#debugging
debug = False
debug_fen = "3B4/5Q1k/8/3p2Pp/8/3p1P2/1PB2P2/4RRK1 b - - 3 51"
debug_playerColour = chess.BLACK

#initialises pygame
pygame.init()
pygame.font.init()

#constants for graphics 
tile_Size = 100 * scale_factor
board_Size = tile_Size*8
#position vector for board 
boardOffset = 10 * scale_factor

#chess pieces are tiled in a png, this holds the coordinates of each piece within the png
piecepositionDict = {"k":(0, 0), "q":(tile_Size, 0), "r":(2*tile_Size, 0), "b":(3*tile_Size, 0), "n":(4*tile_Size, 0), "p":(5*tile_Size, 0),
                     "K":(0, tile_Size), "Q":(tile_Size, tile_Size ), "R":(2*tile_Size, tile_Size), "B":(3*tile_Size, tile_Size), "N":(4*tile_Size, tile_Size), "P":(5*tile_Size, tile_Size)}

#dictionary that holds the values of the piecs
pieceValueDict = {chess.KING:9999, chess.QUEEN:90, chess.ROOK:50, chess.BISHOP:30, chess.KNIGHT: 30, chess.PAWN:10}
                  
columnLetters = ["a", "b", "c", "d", "e", "f", "g", "h"]

#these arrays hold the bonus values for having the pieces at a certain position
pawnvalues = [
    0, 0, 0, 0, 0, 0, 0, 0,
    -3, -3, -3, -2, -2, -3, -3, -3,
    -2, -2, -2, -1, -1, -2, -2, -2,
    -1, 0, 1, 3, 3, 1, 0, -1,
    0, 0, 1, 1, 1, 1, 0, 0,
    1, 1, 1, 2, 2, 1, 1, 1,
    2, 2, 2, 3, 3, 2, 2, 2,
    0, 0, 0, 0, 0, 0, 0, 0]

knightvalues = [
    -5, -4, -3, -2, -2, -3, -4, -5,
    -4, -2, 0, 0, 0, 0, -2, -4,
    -3, 1, 0, 0, 0, 0, 1, -3,
    -2, 0, 0, 3, 3, 0, 0, -2,
    -2, 0, 0, 3, 3, 0, 0, -2,
    -3, 1, 0, 0, 0, 0, 1, -3,
    -4, -2, 0, 0, 0, 0, -2, -4,
    -5, -4, -3, -2, -2, -3, -4, -5]

bishopvalues = [
    -4, -3, -2, 0, 0, -2, -3, -4,
    -3, 0, 0, 0, 0, 0, 0, -3,
    -2, 0, 1, 0, 0, 1, 0, -2,
    0, 0, 0, 2, 2, 0, 0, 0,
    0, 0, 0, 2, 2, 0, 0, 0,
    -2, 0, 1, 0, 0, 1, 0, -2,
    -3, 0, 0, 0, 0, 0, 0, -3,
    -4, -3, -2, 0, 0, -2, -3, -4]

rookvalues = [
    -3, -4, 3, 5, 5, 3, -4, -3,
    -3, 0, 0, 0, 0, 0, 0, -3,
    -3, 0, 0, 0, 0, 0, 0, -3,
    -3, 0, 0, 0, 0, 0, 0, -3,
    -3, 0, 0, 0, 0, 0, 0, -3,
    -3, 0, 0, 0, 0, 0, 0, -3,
    -3, 3, 5, 5, 5, 5, 3, -3,
    -4, 0, 0, 0, 0, 0, 0, -4]

queenvalues = [
    -4, -4, -3, -2, -2, -3, -4, -4,
    -4, 0, 0, 0, 0, 0, 0, -4,
    -3, 0, 2, 3, 3, 2, 0, -3,
    -2, 0, 3, 4, 4, 3, 0, -2,
    -2, 0, 3, 4, 4, 3, 0, -2,
    -3, 0, 2, 3, 3, 2, 0, -3,
    -4, 0, 0, 0, 0, 0, 0, -4,
    -4, -4, -3, -2, -2, -3, -4,-4]

kingvalues = [
    2, 3, 2, 1, 1, 2, 3, 2,
    2, 1, 0, 0, 0, 0, 1, 2,
    0, 0, 0, 0, 0, 0, 0, 0,
    -1, -1, -1, -1, -1, -1, -1, -1,
    -2, -2, -2, -2, -2, -2, -2, -2,
    -3, -3, -3, -3, -3, -3, -3, -3,
    -4, -4, -4, -4, -4, -4, -4, -4,
    -10, -8, -5, -5, -5, -5, -8, -10]

#this dictionary holds the location value arrays for each piece
locationValuesDict = {chess.PAWN:pawnvalues, chess.KNIGHT:knightvalues, chess.BISHOP:bishopvalues,
                      chess.ROOK:rookvalues, chess.QUEEN:queenvalues, chess.KING:kingvalues}
    
#board is the class that represents the chess board
board = chess.Board()

#declarisng variables, will be initisialized by ResetGame
playerColour = None
aiColour = None
flipBoard = None
tileSelected = None
aiMove = None
possibleMoves = None
playerResigned = False
moveHistory = []

def ResetGame():
    board.reset()
    #randomly selects whether player is white or black
    global playerColour
    playerColour = random.choice([chess.WHITE, chess.BLACK])

    if debug:
        board.set_fen(debug_fen)
        playerColour = debug_playerColour
    
    global aiColour
    aiColour = not playerColour
    global flipBoard
    flipBoard = playerColour == chess.BLACK
    global tileSelected
    tileSelected = None
    global possibleMoves
    possibleMoves = []
    global aiMove
    aiMove = None
    global playerResigned
    playerResigned = False
    global moveHistory
    moveHistory = []
    UpdateHistorySurface()



#constants for displaying main screen
scr_Width = 1200 * scale_factor
scr_Height = 1000 * scale_factor
#produces a blank display using the dimensions of the constants
displaySurface = pygame.display.set_mode((scr_Width, scr_Height), 0, 32)
historySurface = pygame.Surface((board_Size, scr_Height - board_Size - boardOffset * 3))
historyFont = pygame.font.Font("Font/Roboto-Regular.ttf", 14)

# Create a function to load and scale images
def load_scaled_image(path, scale_factor):
    image = pygame.image.load(path)
    new_width = int(image.get_width() * scale_factor)
    new_height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (new_width, new_height))

# Load and scale all images using the function
drawScreen = load_scaled_image("drawscreen.png", scale_factor)
victoryScreen = load_scaled_image("victoryscreen.png", scale_factor)
defeatScreen = load_scaled_image("defeatscreen.png", scale_factor)
boardCat = load_scaled_image("cat.png", scale_factor)
resignImage = load_scaled_image("resign.png", scale_factor)
playAgainImage = load_scaled_image("playagain.png", scale_factor)

# Update the playAgainRect after scaling
playAgainRect = playAgainImage.get_rect()
playAgainRect[0] = board_Size + boardOffset * 2
playAgainRect[1] = board_Size * 0.4 + boardOffset
playAgainRect = playAgainImage.get_rect()
playAgainRect[0] = board_Size + boardOffset * 2
playAgainRect[1] = board_Size * 0.4 + boardOffset

#function to print the san move to the move logger below the board
def UpdateHistorySurface():
    historySurface.fill((128, 128, 128))
    moveNumber = 0
    even = True
    #initialises the coordinates for the first move 
    x = 0
    y = 0
    for move in moveHistory:
        if even:
            fontColour = (255, 255, 255)
        else:
            fontColour = (0, 0, 0)
            x = x + 50
        
        tempMoveSurface = historyFont.render(move, True, (fontColour))
        #draws the move to the move logger
        historySurface.blit(tempMoveSurface, (x, y))
        if not even:
            y = y + 25
            x = x - 50
        even = not even
        moveNumber = moveNumber + 1
        if moveNumber == 14:
            moveNumber = 0
            x = x + 100
            y = 0
            
#this function uses the piece values and the board location values to evaluate how good a certain move is
def BoardEval(colour, depth):
    #checks if the board is in either of these draw positions
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    elif board.is_checkmate():
        #depending on which colour has checkmate this is either evaluated to be a good or a bad position
        if board.turn == colour:
            return -999999 + depth * 5000
        else:
            return 999999 - depth * 5000
    else:
        score = 0
        if board.is_check():
            #adds 10 bonus points if the current move puts the opponent in check
            if board.turn == colour:
                score = score - 10
            else:
                score = score + 10
        for pieceType in pieceValueDict:
            value = pieceValueDict[pieceType]
            #matches the piece with the correct location values table
            locationValues = locationValuesDict[pieceType]
            #calculates the score for the current player by subtracting the opposing colour score from the colour score
            for tile in board.pieces(pieceType, colour):
                if colour == chess.BLACK:
                    tile = chess.square_mirror(tile)
                score = score + value + locationValues[tile]
                
            for tile in board.pieces(pieceType, not colour):
                if not colour == chess.BLACK:
                    tile = chess.square_mirror(tile)
                score = score - value - locationValues[tile]
        return score
        
#creates the surface of the board 
def CreateChessBoardSurface():
    surface = pygame.Surface((board_Size, board_Size))
    #fill the board with the dark tile colour then draw the light tiles over it
    surface.fill((80, 80, 80))
    for j in range(0, 8):
        #draw every other tile in each row, offset by 1 on every other row
        for i in [0, 2, 4, 6]:
            if j % 2 ==1:
                i = i + 1
            pygame.draw.rect(surface, (192, 192, 192), (i*tile_Size, j*tile_Size, tile_Size, tile_Size))
    return surface

boardSurface = CreateChessBoardSurface()

#creates a new surface the size of a tile with a specific colour and changes the transparency
def CreateHighlightSurface(colour):
    surface = pygame.Surface((tile_Size, tile_Size))
    surface.set_alpha(128)
    surface.fill(colour)
    return surface

#these are the two different colours used for highlighting original square and target square
highlightSurface = CreateHighlightSurface((255, 255, 102))
selectedSurface = CreateHighlightSurface((32, 178, 170))
aiHighlightSurface = CreateHighlightSurface((255, 51, 51))

#loads in the images needed for the title screen
logo = load_scaled_image("logo.png", scale_factor)
titleText = load_scaled_image("titletext.png", scale_factor)
                             
#this loads the png for the chess pieces
def CreateImagesForPieces():
    image = load_scaled_image("chess.png", scale_factor)
    return pygame.transform.scale(image, (450, 150))

piecesImage = CreateImagesForPieces()

#this detects which tile the user is clicking on
def GetTileFromPosition(position,flipBoard):
    i = position[0] - boardOffset
    j = position[1] - boardOffset
    #this checks if the user clicked out of bounds and if so, returns a null value
    if i < 0 or j < 0:
        return None
    elif i >= board_Size or j >= board_Size:
        return None
    #calculates which tile the user clicked on by dividing the coordinates by the tile size (rounds to an integer)
    i = int(i / tile_Size)
    j = int(j / tile_Size)
    #flips j since graphical coordinates start from the top left
    j = 8-j
    #if player is black this flips all the chess notation coordinates
    if flipBoard == True:
        i = 7 - i
        j = 9 - j
    #returns the chess notation coordinate
    return columnLetters[i]+ str(j)

#fucntion to draw the boxes for the victory screen
def DrawVictoryScreen():
    displaySurface.blit((playAgainImage), (playAgainRect[0], playAgainRect[1]))
    outcome = board.outcome()
    #checks the different end game possibilities and prints a different screen for each one
    if playerResigned == True:
        displaySurface.blit(defeatScreen, (board_Size + boardOffset * 2, boardOffset))
    else:
        if outcome.winner == playerColour:
            displaySurface.blit(victoryScreen, (board_Size + boardOffset * 2, boardOffset))
        elif outcome.winner == None:
            displaySurface.blit(drawScreen, (board_Size + boardOffset * 2, boardOffset))
        else:
            displaySurface.blit(defeatScreen, (board_Size + boardOffset * 2, boardOffset))
    
#temporary function just for testing
def DoAIMoveRandom():
    legal_moves = list(board.legal_moves)
    if legal_moves:
        return random.choice(legal_moves)

#function for the AI to calculate which move is the best from the list of legal moves that have been evaluated
def DoAIMoveBoardEval():
    bestMove = None
    bestScore = -9999999
    #goes through every move possible in the given position
    for move in board.legal_moves:
        score = 0
        #adds 5 bonus points if the move is castling
        if board.is_castling(move):
            score = score + 5
        #pushes the current move to the board
        board.push(move)
        #updates score to the current moves evaluation
        score = score + BoardEval(aiColour, 1)
        #checks if score is greater than bestScore and if it is updates it
        if score > bestScore:
            bestScore = score
            bestMove = move
        #pops the move from the board
        board.pop()
    #pushes the best move to the board
    if bestMove != None:
        return bestMove
    
#minimax function to calculate the max score possible for the individual move
def DoMax(maxDepth, depth, colour, alpha, beta):
    #checks if the depth has reached the terminal node
    if depth == maxDepth or board.is_game_over():
        return BoardEval(colour, depth), None
         
    bestMove = None
    bestScore = -9999999
    #checks all the available legal moves
    for move in board.legal_moves:
        board.push(move)
        score, m = DoMin(maxDepth, depth + 1, colour, alpha, beta)
        if score > bestScore:
            bestScore = score
            bestMove = move
        alpha = max(alpha, score)
        board.pop()
        if score >= beta:
            break
    return bestScore, bestMove

#copy of do max but works for minimum score instead since is calculating the player's moves instead of the AI's
def DoMin(maxDepth, depth, colour, alpha, beta):
    if depth == maxDepth or board.is_game_over():
        return BoardEval(colour, depth), None
         
    bestMove = None
    bestScore = 9999999
    for move in board.legal_moves:
        board.push(move)
        score, m = DoMax(maxDepth, depth + 1, colour, alpha, beta)
        if score < bestScore:
            bestScore = score
            bestMove = move
        beta = min(beta, score)
        board.pop()
        if score <= alpha:
            break
    return bestScore, bestMove

#calls the minimax helper functions 
def DoAIMoveMinimax(maxDepth):
    beta = 9999999999
    alpha = - beta
    bestScore, bestMove = DoMax(maxDepth, 0, aiColour, alpha, beta)
    if bestMove != None:
        return bestMove
    
#finds the coordinates on screen to draw the highlight at
def HighLightSquare(tile, flipBoard, surface):
    row = int(tile[1]) - 1
    column = columnLetters.index(tile[0])
    if flipBoard == True:
        column = 7 - column
    else:
        row = 7 - row
    i = column * tile_Size + boardOffset
    j = row * tile_Size + boardOffset
    displaySurface.blit(surface, (i, j))

#this function handles what happens if anything on the board is clicked
def OnMouseButtonUp(mousePosition):
    global playerResigned
    
    if not board.is_game_over() and playerResigned == False:
        tileClicked = GetTileFromPosition(mousePosition, flipBoard)

        global possibleMoves
        global tileSelected

        if board.turn == playerColour:
            if tileClicked == None:
                tileSelected = None
                possibleMoves = []
                if playAgainRect.collidepoint(mousePosition):
                    playerResigned = True   
            else:
                #gives the number of the square which has been clicked
                square = chess.parse_square(tileClicked)
                #finds what piece is on this square
                pieceAtSquare = board.piece_at(square)
                #checks if player selected their own piece
                if pieceAtSquare != None and pieceAtSquare.color == playerColour:
                    tileSelected = tileClicked
                    #gets all possible legal moves
                    legal_moves = list(board.legal_moves)
                    possibleMoves = []
                    #adds the possible moves which apply to the piece selected to a list
                    for move in legal_moves:
                        if move.from_square == square:
                            possibleMoves.append(move)
                else:
                    #pushed the moves to the board
                    for move in possibleMoves:
                        if move.to_square == square:
                            moveHistory.append(board.san(move))
                            board.push(move)
                            UpdateHistorySurface()
                            global aiMove
                            aiMove = None
                            break
                    #resets the variables after the player has moved
                    tileSelected = None
                    possibleMoves = []
    else:
        if playAgainRect.collidepoint(mousePosition):
            ResetGame()
            
ResetGame()          
running = True
startGame = False
while startGame == False and running == True:
    #prints all the objects required for the title screen
    displaySurface.fill((255, 255, 255))
    logoWidth = logo.get_width()
    logoHeight = logo.get_height()
    displaySurface.blit(logo, ((scr_Width / 2) - (logoWidth / 2), (scr_Height / 2) - (logoHeight / 2)))
    titleTextWidth = titleText.get_width()
    titleTextHeight = titleText.get_height()
    displaySurface.blit(titleText, ((scr_Width / 2) - (titleTextWidth / 2), ((scr_Height / 2) - (titleTextHeight / 2) + (logoHeight*1.5) / 2)))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #ends the running loop
            running = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            startGame = True
    pygame.display.flip()
    
#main loop for game to run
while running == True:
    if not board.is_game_over() and playerResigned == False:
        if board.turn != playerColour:
            #DoAIMoveRandom()
            #DoAIMoveBoardEval()
            maxDepth = 4
            move = DoAIMoveMinimax(maxDepth)
            if move != None:
                aiMove = move.uci()
                moveHistory.append(board.san(move))
                board.push(move)
                UpdateHistorySurface()

    #loop which allows the window to be closed when the x is clicked  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #ends the running loop
            running = False
        #if the event is a mouseclick it calls the mousePosition function to calculate which tile was clicked on
        elif event.type == pygame.MOUSEBUTTONUP:
            OnMouseButtonUp(pygame.mouse.get_pos())
            
    displaySurface.fill((128, 128, 128))
    displaySurface.blit(boardCat, (board_Size - 45, board_Size / 2))
    displaySurface.blit(historySurface, (boardOffset, board_Size + boardOffset * 2))
    #copies the chess board onto the display surface
    displaySurface.blit(boardSurface, (boardOffset, boardOffset))
    displaySurface.blit(resignImage, (playAgainRect[0], playAgainRect[1]))
   
    if tileSelected != None:
        HighLightSquare(tileSelected, flipBoard, selectedSurface)
        for move in possibleMoves:
            uci = move.uci()
            HighLightSquare(uci[2:4], flipBoard, highlightSurface)
    if aiMove != None:
        HighLightSquare(aiMove[2:4], flipBoard, aiHighlightSurface)
        HighLightSquare(aiMove[0:2], flipBoard, aiHighlightSurface)
        
        
    #piece_map lists the positions of all the pieces (from the python-chess library)
    piece_map = board.piece_map()
    #draw each piece
    for index in piece_map:
        #index is the tile number in the tile number in the python-chess library
        #finds the column and row number in vector format from the index
        i = index % 8
        j = (int(index/8))
        #j has been flipped because the first row of the board is at the bottum but graphics coordinates start from the top
        if flipBoard == True:
            i = 7-i
        else:
            j = 7-j
        piece = piece_map[index]
        #symbol is the single character symbol for each chess piece e.g."K" or "k"
        symbol = piece.symbol()
        #finds the position for each piece to be drawn to
        position = (boardOffset + i*tile_Size, boardOffset + j*tile_Size)
        #this finds the piece coordinates in the dictionary and copies the piece from the png
        area = piecepositionDict[symbol] + (tile_Size, tile_Size)
        #copies the piece onto the display surface
        displaySurface.blit(piecesImage, position, area = area)
    if board.is_game_over() or playerResigned == True:
        DrawVictoryScreen()
 
    #swaps the display surface to the screen
    pygame.display.flip()
                
#shuts down pygame when app is exiting
pygame.font.quit()
pygame.quit()
