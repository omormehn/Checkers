from Constants import BOX_SIZE, pygame, CROWN, GREY

class Piece:
    Py = 20
    My = 4
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.King = False
        
        # position
        self.x = 0
        self.y = 0
        
        self.calculate_position()
        
    def calculate_position(self):
        self.x = (BOX_SIZE * self.col) + BOX_SIZE // 2
        self.y = (BOX_SIZE * self.row) + BOX_SIZE // 2
        
        
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()
    
    def make_king(self):
        self.King = True
    
    def draw(self, win):
        radius = BOX_SIZE // 2 - self.Py
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.My)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
        if self.King:
            pygame.draw.circle(win, CROWN, (self.x, self.y), radius // 2)
            
    def __repr__(self):
        return str(self.color)
    

