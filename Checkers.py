from Board import Board
from Constants import pygame, RED, WHITE, GREEN, BOX_SIZE

class Checkers:    
    def __init__(self, win):
        self._init()
        self.win = win
        self.selected = None
        self.turn = RED
        self.valid_moves = {}
        self.score = {RED: 0, WHITE: 0}
        self.winner = None
        self.game_over = False

    
    def _init(self):
        self.board = Board()
        self.score = {RED: 0, WHITE: 0}
        self.game_over = False
        self.winner = None  
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves()
        self.draw_score()
        if self.game_over:
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(f"{self.winner} wins!", True, (255, 255, 255))
            self.win.blit(text, (self.win.get_width() // 2 - text.get_width() // 2, self.win.get_height() // 2 - text.get_height() // 2))
        pygame.display.update()
        
    def reset(self):
        self._init()
        self.selected = None
        self.valid_moves = {}
        self.turn = RED
        
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_man(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
        
        return False
        
    def _move(self, row, col):
        piece = self.board.get_man(row, col)
        print(f"Selected piece: {self.selected}, Target piece: {piece}, Valid moves: {self.valid_moves}")
        
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            
            
            skipped = self.valid_moves[(row, col)]

            if skipped:
                self.board.remove(skipped)
                for skipped_piece in skipped:
                    if skipped_piece.King:
                        self.score[self.turn] += 2
                    else:
                        self.score[self.turn] += 1
                
            self.change_turn()
            
            return True
        
        return False
    
    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        
        if not self.get_valid_moves():
            self.game_over = True
            self.winner = WHITE if self.turn == RED else RED
            return
        
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
            
    def draw_valid_moves(self):
        if self.selected and self.valid_moves:
            for move in self.valid_moves:
                row, col = move
                pygame.draw.circle(self.win, GREEN, (col * BOX_SIZE + BOX_SIZE // 2, row * BOX_SIZE + BOX_SIZE // 2), 15)
                
                
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        if piece.color == RED or piece.King: # ☝️
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        
        if piece.color == WHITE or piece.King: # 👇
            moves.update(self._traverse_left(row + 1, min(row + 3, 8), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, 8), 1, piece.color, right))
        
        return moves
    
    def _traverse_left(self, start, stop, step, color, left, skipped=None):
        if skipped is None:
            skipped = []
        
        moves = {}
        last = []
        
        for row in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board.get_man(row, left)
            
            # If current square is empty
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, left)] = last + skipped
                else:
                    moves[(row, left)] = last
                
                if last:
                    if step == -1:
                        row = max(row - 3, -1)
                    else:
                        row = min(row + 3, 8)
                    
                    moves.update(self._traverse_left(row + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(row + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color != color:
                last = [current]
            # If current square has own piece
            else:
                break
            
            left -= 1
        
        return moves
    def _traverse_right(self, start, stop, step, color, right, skipped=None):
        if skipped is None:
            skipped = []
        
        moves = {}
        last = []
        
        for r in range(start, stop, step):
            if right >= 8:
                break
            
            current = self.board.get_man(r, right)
            
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, 8)
                    
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break

            elif current.color != color:
                last = [current]

            else:
                break
            
            right += 1
        
        return moves
    
    def draw_score(self):
        font = pygame.font.SysFont('comicsans', 20)
    
        red_score_text = font.render(f"RED: {self.score[RED]}", True, RED)
        white_score_text = font.render(f"WHITE: {self.score[WHITE]}", True, WHITE)
        score = Board.evaluate_scores(self.board)
        white_score =  font.render(f"SCORE: {score}", True, ((255, 255, 255)))
        
        
        self.win.blit(red_score_text, (10, 10))  # Top-left corner
        self.win.blit(white_score_text, (10, 50))
        self.win.blit(white_score, (10, 90))