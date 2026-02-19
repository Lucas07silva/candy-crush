import pygame
from pygame.locals import *
import random
import sys

candy_scores = {
    'blue': 30,
    'green': 39,
    'orange': 45,
    'pink': 42,
    'purple': 33,
    'red': 36,
    'teal': 21,
    'yellow': 48
}


score = 0
moves = 0




width = 240  
height = 240  
scoreboard_height = 25
window_size = (width, height + scoreboard_height)


pygame.init()


screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Match Three')


background_color = (255, 255, 255) 

font = pygame.font.Font(None, 24)
text_color = (0, 0, 0) 

# Primeira instrução
instruction1 = font.render("Pressione ENTER para iniciar", True, text_color)
instruction1_rect = instruction1.get_rect()
instruction1_rect.center = (width // 2, height // 2 - 20)

# Segunda instrução
instruction2 = font.render("Maximo de 30 movimentos", True, text_color)
instruction2_rect = instruction2.get_rect()
instruction2_rect.center = (width // 2, height // 2 + 20)


game_started = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_started = True

    screen.fill(background_color)

    if not game_started:
        screen.blit(instruction1, instruction1_rect)
        screen.blit(instruction2, instruction2_rect)
    else:
        width = 240  
        height = 240 
        scoreboard_height = 25
        window_size = (width, height + scoreboard_height)
        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Match Three')

        candy_colors = ['blue', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'yellow']

        candy_width = 40
        candy_height = 40
        candy_size = (candy_width, candy_height)
        

        class Candy:
            
            def __init__(self, row_num, col_num):
                
                self.row_num = row_num
                self.col_num = col_num
                
                self.color = random.choice(candy_colors)
                image_name = f'swirl_{self.color}.png'  
                self.image = pygame.image.load(image_name)
                self.image = pygame.transform.smoothscale(self.image, candy_size)
                self.rect = self.image.get_rect()
                self.rect.left = col_num * candy_width
                self.rect.top = row_num * candy_height
                
            def draw(self):
                screen.blit(self.image, self.rect)
                
            def snap(self):
                self.snap_row()
                self.snap_col()
                
            def snap_row(self):
                self.rect.top = self.row_num * candy_height
                
            def snap_col(self):
                self.rect.left = self.col_num * candy_width
                
        board = []
        for row_num in range(height // candy_height):
            
            board.append([])
            
            for col_num in range(width // candy_width):
                
                candy = Candy(row_num, col_num)
                board[row_num].append(candy)
                
        def draw():
            
            pygame.draw.rect(screen, (173, 216, 230), (0, 0, width, height + scoreboard_height))
            
            for row in board:
                for candy in row:
                    candy.draw()
            
            font = pygame.font.SysFont('monoface', 18)
            score_text = font.render(f'Score: {score}', 1, (0, 0, 0))
            score_text_rect = score_text.get_rect(center=(width / 4, height + scoreboard_height / 2))
            screen.blit(score_text, score_text_rect)
            
            moves_text = font.render(f'Moves: {moves}', 1, (0, 0, 0))
            moves_text_rect = moves_text.get_rect(center=(width * 3 / 4, height + scoreboard_height / 2))
            screen.blit(moves_text, moves_text_rect)
            
        def swap(candy1, candy2):
            
            temp_row = candy1.row_num
            temp_col = candy1.col_num
            
            candy1.row_num = candy2.row_num
            candy1.col_num = candy2.col_num
            
            candy2.row_num = temp_row
            candy2.col_num = temp_col
            
            board[candy1.row_num][candy1.col_num] = candy1
            board[candy2.row_num][candy2.col_num] = candy2
            
            candy1.snap()
            candy2.snap()
            
        def find_matches(candy, matches):
            
            matches.add(candy)
            
            if candy.row_num > 0:
                neighbor = board[candy.row_num - 1][candy.col_num]
                if candy.color == neighbor.color and neighbor not in matches:
                    matches.update(find_matches(neighbor, matches))
                    
            if candy.row_num < height / candy_height - 1:
                neighbor = board[candy.row_num + 1][candy.col_num]
                if candy.color == neighbor.color and neighbor not in matches:
                    matches.update(find_matches(neighbor, matches))
                    
            if candy.col_num > 0:
                neighbor = board[candy.row_num][candy.col_num - 1]
                if candy.color == neighbor.color and neighbor not in matches:
                    matches.update(find_matches(neighbor, matches))
                    
            if candy.col_num < width / candy_width - 1:
                neighbor = board[candy.row_num][candy.col_num + 1]
                if candy.color == neighbor.color and neighbor not in matches:
                    matches.update(find_matches(neighbor, matches))
                    
            return matches
            
        def match_three(candy):
            
            matches = find_matches(candy, set())
            if len(matches) >= 3:
                return matches
            else:
                return set()
                
        clicked_candy = None

        swapped_candy = None

        click_x = None
        click_y = None

        score = 0
        moves = 0

        clock = pygame.time.Clock()
        running = True
        while running:
            
            matches = set()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    
                if clicked_candy is None and event.type == MOUSEBUTTONDOWN:
                    
                    for row in board:
                        for candy in row:
                            if candy.rect.collidepoint(event.pos):
                                
                                clicked_candy = candy
                                
                                click_x = event.pos[0]
                                click_y = event.pos[1]
                                
                if clicked_candy is not None and event.type == MOUSEMOTION:
                    
                    distance_x = abs(click_x - event.pos[0])
                    distance_y = abs(click_y - event.pos[1])
                    
                    if swapped_candy is not None:
                        swapped_candy.snap()
                        
                    if distance_x > distance_y and click_x > event.pos[0]:
                        direction = 'left'
                    elif distance_x > distance_y and click_x < event.pos[0]:
                        direction = 'right'
                    elif distance_y > distance_x and click_y > event.pos[1]:
                        direction = 'up'
                    else:
                        direction = 'down'
                        
                    if direction in ['left', 'right']:
                        clicked_candy.snap_row()
                    else:
                        clicked_candy.snap_col()
                        
                    if direction == 'left' and clicked_candy.col_num > 0:
                        
                        swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num - 1]
                        
                        clicked_candy.rect.left = clicked_candy.col_num * candy_width - distance_x
                        swapped_candy.rect.left = swapped_candy.col_num * candy_width + distance_x
                        
                        if clicked_candy.rect.left <= swapped_candy.col_num * candy_width + candy_width / 4:
                            swap(clicked_candy, swapped_candy)
                            matches.update(match_three(clicked_candy))
                            matches.update(match_three(swapped_candy))
                            moves += 1
                            clicked_candy = None
                            swapped_candy = None
                            
                    if direction == 'right' and clicked_candy.col_num < width / candy_width - 1:
                        
                        swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num + 1]
                        
                        clicked_candy.rect.left = clicked_candy.col_num * candy_width + distance_x
                        swapped_candy.rect.left = swapped_candy.col_num * candy_width - distance_x
                        
                        if clicked_candy.rect.left >= swapped_candy.col_num * candy_width - candy_width / 4:
                            swap(clicked_candy, swapped_candy)
                            matches.update(match_three(clicked_candy))
                            matches.update(match_three(swapped_candy))
                            moves += 1
                            clicked_candy = None
                            swapped_candy = None
                            
                    if direction == 'up' and clicked_candy.row_num > 0:
                        
                        # get the candy above
                        swapped_candy = board[clicked_candy.row_num - 1][clicked_candy.col_num]
                        
                        clicked_candy.rect.top = clicked_candy.row_num * candy_height - distance_y
                        swapped_candy.rect.top = swapped_candy.row_num * candy_height + distance_y
                        
                        if clicked_candy.rect.top <= swapped_candy.row_num * candy_height + candy_height / 4:
                            swap(clicked_candy, swapped_candy)
                            matches.update(match_three(clicked_candy))
                            matches.update(match_three(swapped_candy))
                            moves += 1
                            clicked_candy = None
                            swapped_candy = None
                            
                    if direction == 'down' and clicked_candy.row_num < height / candy_height - 1:
                        
                        swapped_candy = board[clicked_candy.row_num + 1][clicked_candy.col_num]
                        
                        clicked_candy.rect.top = clicked_candy.row_num * candy_height + distance_y
                        swapped_candy.rect.top = swapped_candy.row_num * candy_height - distance_y
                        
                        if clicked_candy.rect.top >= swapped_candy.row_num * candy_height - candy_height / 4:
                            swap(clicked_candy, swapped_candy)
                            matches.update(match_three(clicked_candy))
                            matches.update(match_three(swapped_candy))
                            moves += 1
                            clicked_candy = None
                            swapped_candy = None
            if moves >= 3:
                running = False
                width = 240
                height = 240
                scoreboard_height = 25
                window_size = (width, height + scoreboard_height)

                # Crie uma tela
                screen = pygame.display.set_mode(window_size)
                pygame.display.set_caption("Game Over")
                

                # Defina a pontuação do jogador
                pontuacao = score # Substitua pelo valor da pontuação real

                # Carregue uma fonte para exibir o texto
                font = pygame.font.Font(None, 36)

                # Loop principal
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

                    # Preencha a tela com uma cor de fundo
                    screen.fill((255, 255, 255))

                    score_text = font.render("Pontuação: " + str(pontuacao), True, (0, 0, 0))
                    screen.blit(score_text, (10, height))

                    pygame.display.flip()

                pygame.quit()
                sys.exit()
            
                if clicked_candy is not None and event.type == MOUSEBUTTONUP:
                    
                    clicked_candy.snap()
                    clicked_candy = None
                    if swapped_candy is not None:
                        swapped_candy.snap()
                        swapped_candy = None
                    
            draw()
            pygame.display.update()
            
            if len(matches) >= 3:
                
                 for candy in matches:
                    score += candy_scores[candy.color]/3
                
            while len(matches) > 0:
                    
                    clock.tick(100)
                    
                    for candy in matches:
                        new_width = candy.image.get_width() - 1
                        new_height = candy.image.get_height() - 1
                        new_size = (new_width, new_height)
                        candy.image = pygame.transform.smoothscale(candy.image, new_size)
                        candy.rect.left = candy.col_num * candy_width + (candy_width - new_width) / 2
                        candy.rect.top = candy.row_num * candy_height + (candy_height - new_height) / 2
                        
                    for row_num in range(len(board)):
                        for col_num in range(len(board[row_num])):
                            candy = board[row_num][col_num]
                            if candy.image.get_width() <= 0 or candy.image.get_height() <= 0:
                                matches.remove(candy)
                                
                                board[row_num][col_num] = Candy(row_num, col_num)
                                
                    draw()
                    pygame.display.update()
                    
        pygame.quit()

        pass

    pygame.display.flip()
    

pygame.quit()
