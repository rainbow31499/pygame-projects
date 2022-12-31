import os
import pygame
from colorit import init_colorit, color, background, Colors

class ChessGame:
    def __init__(self):
        self.board = 'RNBQKBNRPPPPPPPP                                pppppppprnbqkbnr' # String of length 64 to represent the board's pieces
        self.turn = 0 # 0 for white, 1 for black
        self.white_kcastle = True # Allow kingside castling
        self.white_qcastle = True # Allow queenside castling
        self.black_kcastle = True # Allow kingside castling
        self.black_qcastle = True # Allow queenside castling
        self.en_passant = None # Indicate file of pawn (0 (a) to 7 (h)) moved two spaces to allow en passant capture
        self.captured_pieces = []
        self.promotion = None # Indicate file of pawn (0 (a) to 7 (h)) if on top rank
        self.running = True # Game is running
        self.move_no = 1
        self.move_history = []
        self.result = None # Result at end of game: 1 = White wins, -1 = Black wins, 0 = Draw

    def __str__(self):
        board_colors = {0: (155,155,155), 1: (100,100,100)}
        piece_colors = {0: (255,255,255), 1: (0,0,0)}
        board = ''''''
        for rank in range(8):
            for file in range(8):
                if self.board[file+8*rank].islower():
                    piece_color = 0
                elif self.board[file+8*rank].isupper():
                    piece_color = 1
                board += background(color(' '+self.board[file+8*rank]+' ', piece_colors[piece_color]), board_colors[(rank+file)%2])
            board += '\n'
        
        return board

    def convert_square_to_number(self, square):
        file = square[0]
        rank = square[1]
        converted = (ord(file)-97)+8*(8-int(rank))
        return converted

    def convert_number_to_square(self, number):
        file = number % 8
        rank = number // 8
        converted = chr(97+file) + str(8-rank)
        return converted

    def piece_on_square(self, square):
        if type(square) == int:
            return self.board[square]
        elif type(square) == str:
            return self.board[self.convert_square_to_number(square)]

    def move(self, mov):
        moved_piece = self.piece_on_square(mov[0])
        captured_piece = self.piece_on_square(mov[1])

        # White kingside castling
        if mov == (60,62) and self.board[60] == 'k':
            new_board = self.board[:60] + ' rk '

        # White queenside castling
        elif mov == (60,58) and self.board[60] == 'k':
            new_board = self.board[:56] + '  kr ' + self.board[61:]

        # Black kingside castling
        elif mov == (4,6) and self.board[4] == 'K':
            new_board = self.board[:4] + ' RK ' + self.board[8:]

        # Black queenside castling
        elif mov == (4,2) and self.board[4] == 'K':
            new_board = '  KR ' + self.board[5:]

        else:
            new_board = self.board[:(mov[0])] + ' ' + self.board[(mov[0]+1):]
            new_board = new_board[:(mov[1])] + moved_piece + new_board[(mov[1]+1):]
            
            # En passant only
            if moved_piece.lower() == 'p' and (abs(mov[1] - mov[0]) in [7,9]) and captured_piece == ' ':
                if moved_piece.islower(): # by white
                    new_board = new_board[:(mov[1]+8)] + ' ' + new_board[(mov[1]+8+1):]
                    captured_piece = 'P'
                elif moved_piece.isupper(): # by black
                    new_board = new_board[:(mov[1]-8)] + ' ' + new_board[(mov[1]-8+1):]
                    captured_piece = 'p'
        
        return {'board': new_board, 'captured_piece': captured_piece}

    def promote(self, new_piece):
        if self.turn == 0 and self.promotion != None:
            new_board = self.board[:(self.promotion)] + new_piece.lower() + self.board[(self.promotion+1):]
        elif self.turn == 1 and self.promotion != None:
            new_board = self.board[:(56+self.promotion)] + new_piece.upper() + self.board[(56+self.promotion+1):]
        
        self.board = new_board

        self.promotion = None
        self.turn = int(not(self.turn))

    def possible_moves(self, turn=None):
        if turn == None:
            turn = self.turn

        moves = []
        for rank in range(8):
            for file in range(8):
                position_number = file+8*rank
                position_square = self.convert_number_to_square(position_number)
                piece = self.board[position_number]

                if turn == 0:
                    if piece.islower() == False:
                        continue
                elif turn == 1:
                    if piece.isupper() == False:
                        continue

                if piece == 'p':
                    if rank == 6:
                        for spaces in [1,2]:
                            new_position = file+8*(rank-spaces)
                            if self.board[new_position] == ' ':
                                moves.append((position_number, new_position))
                            else:
                                break
                    else:
                        if 0 <= rank-1 <= 7:
                            new_position = file+8*(rank-1)
                            if self.board[new_position] == ' ':
                                moves.append((position_number, new_position))
                    for spaces in [-1,1]:
                        if 0 <= file+spaces <= 7 and 0 <= rank-1 <= 7:
                            new_position = (file+spaces)+8*(rank-1)
                            if self.board[new_position].isupper():
                                moves.append((position_number, new_position))
                            if self.en_passant == file+spaces and rank == 3:
                                new_position = (file+spaces)+8*(rank-1)
                                if self.board[new_position+8].isupper():
                                    moves.append((position_number, new_position))
                
                elif piece == 'P':
                    if rank == 1:
                        for spaces in [1,2]:
                            new_position = file+8*(rank+spaces)
                            if self.board[new_position] == ' ':
                                moves.append((position_number, new_position))
                            else:
                                break
                    else:
                        if 0 <= rank+1 <= 7:
                            new_position = file+8*(rank+1)
                            if self.board[new_position] == ' ':
                                moves.append((position_number, new_position))
                    for spaces in [-1,1]:
                        if 0 <= file+spaces <= 7 and 0 <= rank+1 <= 7:
                            new_position = (file+spaces)+8*(rank+1)
                            if self.board[new_position].islower():
                                moves.append((position_number, new_position))
                            if self.en_passant == file+spaces and rank == 4:
                                new_position = (file+spaces)+8*(rank+1)
                                if self.board[new_position-8].islower():
                                    moves.append((position_number, new_position))

                elif piece.lower() == 'n':
                    for x in [-2,-1,1,2]:
                        for y in [-2,-1,1,2]:
                            if abs(x) + abs(y) == 3:
                                if 0 <= file + x <= 7 and 0 <= rank + y <= 7:
                                    new_position = (file+x)+8*(rank+y)
                                    if piece.islower():
                                        if self.board[new_position].isupper() or self.board[new_position] == ' ':
                                            moves.append((position_number, new_position))
                                    elif piece.isupper():
                                        if self.board[new_position].islower() or self.board[new_position] == ' ':
                                            moves.append((position_number, new_position))

                elif piece.lower() == 'b':
                    for x in [-1,1]:
                        for y in [-1,1]:
                            spaces = 1
                            while spaces <= 8:
                                if 0 <= file + x*spaces <= 7 and 0 <= rank + y*spaces <= 7:
                                    new_position = (file+x*spaces)+8*(rank+y*spaces)
                                    if self.board[new_position] == ' ':
                                        moves.append((position_number, new_position))
                                    else:
                                        if piece.islower():
                                            if self.board[new_position].isupper():
                                                moves.append((position_number, new_position))
                                        elif piece.isupper():
                                            if self.board[new_position].islower():
                                                moves.append((position_number, new_position))
                                        break
                                else:
                                    break
                                spaces += 1
                
                elif piece.lower() == 'r':
                    for x in [-1,0,1]:
                        for y in [-1,0,1]:
                            if abs(x) + abs(y) == 1:
                                spaces = 1
                                while spaces <= 8:
                                    if 0 <= file + x*spaces <= 7 and 0 <= rank + y*spaces <= 7:
                                        new_position = (file+x*spaces)+8*(rank+y*spaces)
                                        if self.board[new_position] == ' ':
                                            moves.append((position_number, new_position))
                                        else:
                                            if piece.islower():
                                                if self.board[new_position].isupper():
                                                    moves.append((position_number, new_position))
                                            elif piece.isupper():
                                                if self.board[new_position].islower():
                                                    moves.append((position_number, new_position))
                                            break
                                    else:
                                        break
                                    spaces += 1

                elif piece.lower() == 'q':
                    for x in [-1,0,1]:
                        for y in [-1,0,1]:
                            if abs(x) + abs(y) > 0:
                                spaces = 1
                                while spaces <= 8:
                                    if 0 <= file + x*spaces <= 7 and 0 <= rank + y*spaces <= 7:
                                        new_position = (file+x*spaces)+8*(rank+y*spaces)
                                        if self.board[new_position] == ' ':
                                            moves.append((position_number, new_position))
                                        else:
                                            if piece.islower():
                                                if self.board[new_position].isupper():
                                                    moves.append((position_number, new_position))
                                            elif piece.isupper():
                                                if self.board[new_position].islower():
                                                    moves.append((position_number, new_position))
                                            break
                                    else:
                                        break
                                    spaces += 1

                elif piece.lower() == 'k':
                    for x in [-1,0,1]:
                        for y in [-1,0,1]:
                            if abs(x) + abs(y) >= 0:
                                if 0 <= file + x <= 7 and 0 <= rank + y <= 7:
                                    new_position = (file+x)+8*(rank+y)
                                    if self.board[new_position] == ' ':
                                        moves.append((position_number, new_position))
                                    else:
                                        if piece.islower():
                                            if self.board[new_position].isupper():
                                                moves.append((position_number, new_position))
                                        elif piece.isupper():
                                            if self.board[new_position].islower():
                                                moves.append((position_number, new_position))
                    
                    if piece.islower():
                        if self.white_kcastle == True and self.board[61:63] == '  ':
                            moves.append((60,62))
                        if self.white_qcastle == True and self.board[57:60] == '   ':
                            moves.append((60,58))
                    elif piece.isupper():
                        if self.black_kcastle == True and self.board[5:7] == '  ':
                            moves.append((4,6))
                        if self.black_qcastle == True and self.board[1:4] == '   ':
                            moves.append((4,2))

        return moves

    def check(self, side=None, board=None):
        # Is the king on side 0 (white) or 1 (black) in check?

        if side == None:
            side = self.turn

        if board == None:
            board = self.board

        checked = False

        for position in range(64):
            piece = board[position]

            if side == 0 and piece == 'k':
                king_position = position
                break
                
            if side == 1 and piece == 'K':
                king_position = position
                break
        
        test_game = ChessGame()
        test_game.board = board
        test_game.turn = int(not side)

        for move in test_game.possible_moves():
            if move[1] == king_position:
                checked = True
        
        return checked

    def legal_moves(self, turn=None):
        if turn == None:
            turn = self.turn

        legal_moves = []
        for mov in self.possible_moves(turn):
            if self.check(board=self.move(mov)['board']) == False:
                if self.board[60] == 'k' and mov == (60,62):
                    if self.check(side=0) == False and self.check(board=self.move((60,61))['board'], side=0) == False:
                        legal_moves.append((60,62))
                elif self.board[60] == 'k' and mov == (60,58):
                    if self.check(side=0) == False and self.check(board=self.move((60,59))['board'], side=0) == False:
                        legal_moves.append((60,58))
                elif self.board[4] == 'K' and mov == (4,6):
                    if self.check(side=1) == False and self.check(board=self.move((4,5))['board'], side=1) == False:
                        legal_moves.append((4,6))
                elif self.board[4] == 'K' and mov == (4,2):
                    if self.check(side=1) == False and self.check(board=self.move((4,3))['board'], side=1) == False:
                        legal_moves.append((4,2))
                else:
                    legal_moves.append(mov)

        return legal_moves

    def notate_moves(self):
        notation = {move: '' for move in self.legal_moves()}

        for move in notation:
            if self.board[move[0]].lower() == 'p':
                if abs(move[0]-move[1]) % 8 == 0:
                    notation[move] = self.convert_number_to_square(move[1])
                elif abs(move[0]-move[1]) in [7,9]:
                    notation[move] = self.convert_number_to_square(move[0])[0] + 'x' + self.convert_number_to_square(move[1])
            elif self.board[move[0]] == 'k' and move in [(60,62),(60,58)]:
                if move == (60,62):
                    notation[move] = 'O-O'
                elif move == (60,58):
                    notation[move] = 'O-O-O'
            elif self.board[move[0]] == 'K' and move in [(4,6),(4,2)]:
                if move == (4,6):
                    notation[move] = 'O-O'
                elif move == (4,2):
                    notation[move] = 'O-O-O'
            else:
                if self.piece_on_square(move[1]) == ' ':
                    notation[move] = self.piece_on_square(move[0]).upper() + self.convert_number_to_square(move[1])
                elif self.piece_on_square(move[1]) != ' ':
                    notation[move] = self.piece_on_square(move[0]).upper() + 'x' + self.convert_number_to_square(move[1])

        occurrences = {}

        for move in notation:
            if notation[move] not in occurrences:
                occurrences[notation[move]] = 1
            else:
                occurrences[notation[move]] += 1

        duplicates = list(filter(lambda note: occurrences[note] >= 2, occurrences))

        # Resolve duplicated notation
        for note in duplicates:
            moves = list(filter(lambda move: notation[move] == note, notation))
            origins = map(lambda move: self.convert_number_to_square(move[0]), moves)
            
            file_count = {}
            rank_count = {}
            for origin in origins:
                file = origin[0]
                if file not in file_count:
                    file_count[file] = 1
                else:
                    file_count[file] += 1
                rank = origin[1]
                if rank not in rank_count:
                    rank_count[rank] = 1
                else:
                    rank_count[rank] += 1
            duplicated_files = list(filter(lambda file: file_count[file] >= 2, file_count))
            duplicated_ranks = list(filter(lambda rank: rank_count[rank] >= 2, rank_count))

            for move in moves:
                file = self.convert_number_to_square(move[0])[0]
                rank = self.convert_number_to_square(move[0])[1]
                if file in duplicated_files and rank in duplicated_ranks:
                    new_note = note[0] + file + rank + note[1:]
                elif file in duplicated_files:
                    new_note = note[0] + rank + note[1:]
                else:
                    new_note = note[0] + file + note[1:]
                
                notation[move] = new_note

        for move in notation:
            test_game = ChessGame()
            test_game.board = self.board
            test_game.turn = self.turn
            test_game.board = self.move(move)['board']
            test_game.turn = int(not(self.turn))
            if test_game.check() == True:
                if test_game.legal_moves() == []:
                    notation[move] += '#'
                else:
                    notation[move] += '+'

        return notation

    def run_move(self, mov):
        if mov in self.legal_moves():
            self.move_history.append(self.notate_moves()[mov])
            if self.turn == 0:
                pass
            #    print(str(self.move_no) + '. ' + self.notate_moves()[mov])
            elif self.turn == 1:
            #    print('... ' + self.notate_moves()[mov])
                self.move_no += 1

            # Update castling
            if self.board[mov[0]] == 'k':
                self.white_kcastle = False
                self.white_qcastle = False
            if self.board[mov[0]] == 'K':
                self.black_kcastle = False
                self.black_qcastle = False
            
            if self.board[mov[0]] == 'r':
                if mov[0] == 56:
                    self.white_qcastle = False
                elif mov[0] == 63:
                    self.white_kcastle = False
            if self.board[mov[0]] == 'R':
                if mov[0] == 0:
                    self.black_qcastle = False
                elif mov[0] == 7:
                    self.black_kcastle = False

            # En passant if pawn moves two spaces
            if self.board[mov[0]].lower() == 'p' and abs(mov[1]-mov[0]) == 16:
                self.en_passant = mov[0] % 8
            else:
                self.en_passant = None

            # Promote if pawn moves to top rank
            if (self.board[mov[0]] == 'p' and 0 <= mov[1] <= 7) or (self.board[mov[0]] == 'P' and 56 <= mov[1] <= 63):
                self.promotion = mov[1] % 8
            else:
                self.promotion = None

            if self.promotion == None:
                self.turn = int(not(self.turn))

            self.board, captured_piece = self.move(mov)['board'], self.move(mov)['captured_piece']

            if captured_piece != ' ':
                self.captured_pieces.append(captured_piece)

            if self.legal_moves() == []:
                self.running = False
                if self.check(side=0) == True:
                    self.result = -1
                elif self.check(side=1) == True:
                    self.result = 1
                else:
                    self.result = 0

game = ChessGame()
assert(game.convert_square_to_number('d6') == 19)
assert(game.convert_square_to_number('d5') == 27)
assert(game.convert_square_to_number('g5') == 30)
assert(game.convert_number_to_square(19) == 'd6')
assert(game.convert_number_to_square(27) == 'd5')
assert(game.convert_number_to_square(30) == 'g5')
assert(game.piece_on_square('e8') == 'K')
assert(game.piece_on_square(60) == 'k')

assert((49,41) in game.possible_moves())
assert(game.notate_moves()[(49,41)] == 'b3')
assert((50,34) in game.possible_moves())
assert(game.notate_moves()[(50,34)] == 'c4')
assert((57,42) in game.possible_moves())
assert(game.notate_moves()[(57,42)] == 'Nc3')
assert((62,45) in game.possible_moves())
assert(game.notate_moves()[(62,45)] == 'Nf3')

assert(game.move((49,41))['board'] == 'RNBQKBNRPPPPPPPP                         p      p pppppprnbqkbnr')
assert(game.move((57,42))['board'] == 'RNBQKBNRPPPPPPPP                          n     ppppppppr bqkbnr')

test_game_1 = ChessGame()
test_game_1.board = 'R B  RK PP  BPPP  N P   Q      N  b  b  p n pn   pq  ppp   rk  r'
test_game_1.turn = 1 # Test position 1 with black to move

assert(test_game_1.check(board='R B  RK PP  BPPP  N P          N  b  b  p Q pn   pq  ppp   rk  r',side=0) == True)
assert(test_game_1.check(board='R B  RK PP  BPPP  N P          N Qb  b  p n pn   pq  ppp   rk  r',side=0) == False)
assert(test_game_1.check(board='R B  RK PP  BPPP  N P          N  Q  b  p n pn   pq  ppp   r k r',side=0) == True)

assert((20,28) in test_game_1.legal_moves())
assert((24,42) in test_game_1.legal_moves())

test_game_2 = ChessGame()
test_game_2.board = ' Q N RK  R    PP    PBN  BP p   q       r n  n       ppp  b  rk '
test_game_2.turn = 0 # Test position 2 with white to move

assert((42,25) in test_game_2.legal_moves())
assert(test_game_2.notate_moves()[(42,25)] == 'Nxb5')
assert((28,21) in test_game_2.legal_moves())
assert(test_game_2.notate_moves()[(28,21)] == 'exf6')
assert((61,59) in test_game_2.legal_moves())
assert(test_game_2.notate_moves()[(61,59)] == 'Rd1')

test_game_3 = ChessGame()
test_game_3.board = '   N RK       PPq   P     P Q       RB     r p       pk   br    '
test_game_3.turn = 0 # Test position 3 with white to move

assert((59,51) in test_game_3.legal_moves())
assert(test_game_3.notate_moves()[(59,51)] == 'R1d2')
assert((43,51) in test_game_3.legal_moves())
assert(test_game_3.notate_moves()[(43,51)] == 'R3d2')

test_game_4 = ChessGame()
test_game_4.board = 'QRBN RK P PPB PP    P N  p      q    P    n p n   pp pppr b kbr '
test_game_4.turn = 0 # Test position 4 with white to move

assert((42,52) in test_game_4.legal_moves())
assert(test_game_4.notate_moves()[(42,52)] == 'Nce2')
assert((46,52) in test_game_4.legal_moves())
assert(test_game_4.notate_moves()[(46,52)] == 'Nge2')

test_game_5 = ChessGame()
test_game_5.board = ' K      Pp     r          PP p           pB  n p R   N    k   r '
test_game_5.turn = 1 # Test position 5 with black to move

assert((53,43) in test_game_5.legal_moves())
assert(test_game_5.notate_moves()[(53,43)] == 'Nd3+')

test_game_6 = ChessGame()
test_game_6.board = 'R BQKB RPPPP PPP  N  N      P  q  b p           pppp ppprnb k nr'
test_game_6.turn = 0 # Test position 6 with white to move (a mate in 1)

assert((31,13) in test_game_6.legal_moves())
assert(test_game_6.notate_moves()[(31,13)] == 'Qxf7#')

pygame.init()

screen = pygame.display.set_mode([540,600])

active_square = None

pygame_running = True

while pygame_running == True:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.promotion == None:
                if 30 <= event.pos[0] < 510 and 60 <= event.pos[1] < 540 and game.running == True:
                    clicked_square = ((event.pos[0] - 30) // 60) + ((event.pos[1] - 60) // 60) * 8
                    if (game.turn == 0 and game.board[clicked_square].islower()) or (game.turn == 1 and game.board[clicked_square].isupper()):
                        active_square = clicked_square
                    else:
                        if active_square != None:
                            game.run_move((active_square, clicked_square))
                            active_square = None
            else:
                pieces = ['n', 'b', 'r', 'q']
                if 210 <= event.pos[1] < 270:
                    for x in range(4):
                        if 210 + 80 * x <= event.pos[0] < 270 + 80 * x:
                            game.promote(pieces[x])

    for x in range(8):
        for y in range(8):
            piece = game.board[x+8*y]

            if active_square == x+8*y:
                square_color = (128,192,192)
            elif (game.check() == True and game.turn == 0 and piece == 'k') or \
                (game.check() == True and game.turn == 1 and piece == 'K'):
                square_color = (255,0,0)
            else:
                if (x+y)%2 == 0:
                    square_color = (192,192,192)
                elif (x+y)%2 == 1:
                    square_color = (128,128,128)
                    
            pygame.draw.rect(screen, square_color, pygame.Rect(30+60*x,60+60*y,60,60))
            
            if piece.islower():
                piece_color = 'w'
            elif piece.isupper():
                piece_color = 'b'

            directory = os.getcwd()
            if piece != ' ':
                image_source = (piece.lower() + piece_color + '.png')
                piece_image = pygame.image.load(image_source)
                screen.blit(piece_image, (30+60*x,60+60*y))

    black_captured_pieces = 0
    white_captured_pieces = 0
    for piece in game.captured_pieces:
        if piece.islower():
            piece_color = 'w'
        elif piece.isupper():
            piece_color = 'b'

        image_source = (piece.lower() + piece_color + '.png')
        piece_image = pygame.image.load(image_source)
        piece_image = pygame.transform.scale(piece_image, (30,30))

        if piece.islower():
            screen.blit(piece_image, (50+20*white_captured_pieces,550))
            white_captured_pieces += 1
        elif piece.isupper():
            screen.blit(piece_image, (50+20*black_captured_pieces,20))
            black_captured_pieces += 1

    if game.promotion != None:
        piece_location = 200
        for piece in ['n', 'b', 'r', 'q']:
            if game.turn == 0:
                piece_color = 'w'
            elif game.turn == 1:
                piece_color = 'b'
            image_source = os.path.join(directory, (piece.lower() + piece_color + '.png'))
            piece_image = pygame.image.load(image_source)
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(piece_location,200,80,80))
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(piece_location+10,210,60,60))
            screen.blit(piece_image, (piece_location+10,210))
            piece_location += 80

    if game.running == False:
        if game.result == 1:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(70,250,400,100))
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(80,260,380,80))
        elif game.result == -1:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(70,250,400,100))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(80,260,380,80))
        elif game.result == 0:
            pygame.draw.rect(screen, (128,128,128), pygame.Rect(70,250,400,100))
            pygame.draw.rect(screen, (128,128,128), pygame.Rect(80,260,380,80))

    pygame.display.flip()

pygame.quit()

print(game.move_history)