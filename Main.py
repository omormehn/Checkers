
from Constants import pygame, WIDTH, HEIGHT, BOX_SIZE
from Checkers import Checkers


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def main():
    run = True
    clock = pygame.time.Clock()
    checkers = Checkers(WIN)
    
    while run: 
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                row, col = pos[1] // BOX_SIZE, pos[0] // BOX_SIZE
                checkers.select(row, col)
    
        checkers.update()
    pygame.quit()
    
    
if __name__ == '__main__':
    main()