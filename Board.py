from Constants import BLACK, BROWN, ROWS, COL, BOX_SIZE, WHITE, RED, pygame
from Piece import Piece
class Board(Piece):
    def __init__(self):
        self.board = []
        self.white_pieces_left = self.red_pieces_left = 12
        self.white_kings = self.red_kings = 0
        self.add_men()
        
    def evaluate_scores(self):
        return self.red_pieces_left - self.white_pieces_left + (self.red_kings * 0.5 - self.white_kings * 0.5)
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, BROWN, (col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE, BOX_SIZE))

    def get_men(self, color):
        pieces = []
        for row in self.board:
            for man in row:
                if man != 0 and man.color == color:
                    pieces.append(man)
        return pieces
    
    def get_man(self, row, col):
        return self.board[row][col]
    
    def move(self, man, row, col):
        # movement across board
        self.board[man.row][man.col], self.board[row][col] = self.board[row][col], self.board[man.row][man.col]
        man.move(row, col)
        
        # make king
        if row == ROWS - 1 or row == 0:
            man.make_king()
            if man.color == WHITE:
                self.white_kings += 1
            else: 
                self.red_kings += 1
                
    # create board
    def add_men(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COL):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        piece = Piece(row, col, WHITE)
                        self.board[row].append(piece)
                    elif row > 4:
                        piece = Piece(row, col, RED)
                        self.board[row].append(piece)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
            
    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COL):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == RED:
                self.red_pieces_left -= 1
            else:
                self.white_pieces_left -= 1