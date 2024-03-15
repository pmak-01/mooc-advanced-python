from random import randint, choice

import pygame
pygame.init()

class Game:
    '''A class to control the working of the game, such as counting points and drawing elements'''

    red = (255, 60, 0)
    green = (0, 255, 0)
    blue = (0, 170, 255)
    white = (255, 255, 255)
    grey = (35, 38, 50)
    black = (0, 0, 0)
    yellow = (255, 255, 51)
    pastel_green = (77, 255, 0)

    screen_width, screen_height = 1024, 600
    dir = {'left': 0, # a dictionary to map direction with index, avoiding confusion
           'right': 1,
           'up': 2,
           'down': 3}
    max_coins = 20 # the number of coins that will be produced in this game

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont('Consolas', 24)
        self.no_font = pygame.font.SysFont('Consolas', 0) # a font that will hide text that uses this font
        self.large_font = pygame.font.SysFont('Consolas', 48)

        self.window = pygame.display.set_mode((Game.screen_width, Game.screen_height))
        pygame.display.set_caption('Orb Wars')

        self.monster = pygame.image.load('src/monster.png')
        self.monster_dimen = self.monster.get_width(), self.monster.get_height()

        self.coin = pygame.image.load('src/coin.png')
        self.coin_dimen = self.coin.get_width(), self.coin.get_height()

        self.crown = pygame.image.load('src/crown.png') # image taken from https://www.iconexperience.com/g_collection/icons/?icon=crown
        self.crown_dimen = self.crown.get_width(), self.crown.get_height()

        init_radius = 20 # initial radius of both players' circles
        self.player1 = Player((self.screen_width-init_radius, self.screen_height-init_radius), Game.red, init_radius, 10)
        self.player2 = Player((init_radius, init_radius), Game.blue, init_radius, 10)

        self.p1_states = [[False, self.player1.move_left], [False, self.player1.move_right], [False, self.player1.move_up], [False, self.player1.move_down]]
        self.p2_states = [[False, self.player2.move_left], [False, self.player2.move_right], [False, self.player2.move_up], [False, self.player2.move_down]]
        # these lists store tuple elements of form (bool, function), to denote whether the player is moving in a direction and the respective function

        self.coin_positions = [] # coordinates of all coins present on the screen
        self.coin_count = 0 # number of coins collected in the game at that point

        self.game_state = {'intro': True, 'play': False, 'end': False}

    def main_loop(self):
        while True:
            self.check_events()
            if self.game_state['intro']:
                self.show_intro_screen()
            
            elif self.game_state['play']:
                self.move_players()
                self.add_coins()
                self.update_points()
                self.draw_elements()
                self.check_end()
            
            elif self.game_state['end']:
                self.draw_end_screen()

            self.clock.tick(60)

    def show_intro_screen(self):
        '''Printing the initial instruction for the players to know what the game is about'''
        self.window.fill(Game.pastel_green)
        curr_font = pygame.font.SysFont('Verdana', 50)

        txt1 = curr_font.render(f"Player Red moves with arrow keys", False, Game.red)
        txt2 = curr_font.render(f"Player Blue moves with WASD keys", False, Game.blue)
        txt3 = curr_font.render(f"Players grow larger by collecting coins", False, Game.grey)
        txt4 = curr_font.render(f"{Game.max_coins} coins can be collected in this game", False, Game.grey)
        txt5 = curr_font.render(f"Goal: Collect as many coins as possible", False, Game.grey)
        txt6 = curr_font.render(f"Press Space to begin!", False, Game.grey)

        txts = [txt1, txt2, txt3, txt4, txt5, txt6]

        for i, y in zip(range(0,6), range(20, 100000, txt1.get_height()+10)):
            self.window.blit(txts[i], ((Game.screen_width-txts[i].get_width())//2, y))

        pygame.display.flip()

    def dist_betwn_pts(pt1: list, pt2: list):
        '''Returns Manhattan distance between two points'''
        ans = abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
        return ans

    def check_events(self):
        '''Checks for keypresses'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.p1_states[Game.dir['left']][0] = True
                if event.key == pygame.K_RIGHT:
                    self.p1_states[Game.dir['right']][0] = True
                if event.key == pygame.K_UP:
                    self.p1_states[Game.dir['up']][0] = True
                if event.key == pygame.K_DOWN:
                    self.p1_states[Game.dir['down']][0] = True

                if event.key == pygame.K_a:
                    self.p2_states[Game.dir['left']][0] = True
                if event.key == pygame.K_d:
                    self.p2_states[Game.dir['right']][0] = True
                if event.key == pygame.K_w:
                    self.p2_states[Game.dir['up']][0] = True
                if event.key == pygame.K_s:
                    self.p2_states[Game.dir['down']][0] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.p1_states[Game.dir['left']][0] = False
                if event.key == pygame.K_RIGHT:
                    self.p1_states[Game.dir['right']][0] = False
                if event.key == pygame.K_UP:
                    self.p1_states[Game.dir['up']][0] = False
                if event.key == pygame.K_DOWN:
                    self.p1_states[Game.dir['down']][0] = False

                if event.key == pygame.K_a:
                    self.p2_states[Game.dir['left']][0] = False
                if event.key == pygame.K_d:
                    self.p2_states[Game.dir['right']][0] = False
                if event.key == pygame.K_w:
                    self.p2_states[Game.dir['up']][0] = False
                if event.key == pygame.K_s:
                    self.p2_states[Game.dir['down']][0] = False

                if event.key == pygame.K_SPACE and self.game_state['intro']:
                    self.game_state['intro'] = False
                    self.game_state['play'] = True

                if event.key == pygame.K_SPACE and self.game_state['end']:
                    exit()

    def move_players(self):
        '''Controls player movement'''
        for state, func in self.p1_states:
            if state: func()
        for state, func in self.p2_states:
            if state: func()

    def add_coins(self):
        '''Adds new coins at a random position'''
        if len(self.coin_positions) > 5 or self.coin_count > Game.max_coins:
            return
        
        newPos = [randint(0, Game.screen_width-self.coin_dimen[0]), randint(0, Game.screen_height-self.coin_dimen[1])]

        self.coin_positions.append(newPos)

    def update_points(self):
        '''Increases points if coin is collected'''
        to_remove = []

        for coin_pos in self.coin_positions:
            coin_center = list((coin_pos[0] + self.coin_dimen[0]//2, coin_pos[1] + self.coin_dimen[1]//2))
            
            if Game.dist_betwn_pts(coin_center, self.player1.center_pos) <= self.player1.radius:
                self.player1.add_point()
                self.player1.increase_radius(1)
                self.coin_count += 1
                to_remove.append(coin_pos)

                print(f'P1: {self.player1.points}, P2: {self.player2.points}')
            
            elif Game.dist_betwn_pts(coin_center, self.player2.center_pos) <= self.player2.radius:
                self.player2.add_point()
                self.player2.increase_radius(1)
                self.coin_count += 1
                to_remove.append(coin_pos)

                print(f'P1: {self.player1.points}, P2: {self.player2.points}')

        for pos in to_remove:
            if pos in self.coin_positions:
                self.coin_positions.remove(pos)

    def draw_elements(self):
        '''Draws all game elements onto the screen'''
        self.window.fill(Game.grey)
        
        pygame.draw.circle(self.window, self.player1.color, self.player1.center_pos, self.player1.radius)
        pygame.draw.circle(self.window, self.player2.color, self.player2.center_pos, self.player2.radius)

        for coin_pos in self.coin_positions:
            self.window.blit(self.coin, coin_pos)

        p1_points_holder = self.game_font.render(f"{self.player1.points}", False, Game.white)
        p2_points_holder = self.game_font.render(f"{self.player2.points}", False, Game.white)
        rem_coins_holder = self.game_font.render(f"Remaining coins: {Game.max_coins-self.coin_count}", False, Game.yellow)

        self.window.blit(p1_points_holder, (self.player1.center_pos[0]-p1_points_holder.get_width()//2, self.player1.center_pos[1]-p1_points_holder.get_height()//2))
        self.window.blit(p2_points_holder, (self.player2.center_pos[0]-p2_points_holder.get_width()//2, self.player2.center_pos[1]-p2_points_holder.get_height()//2))
        self.window.blit(rem_coins_holder, (Game.screen_width//2 - rem_coins_holder.get_width()//2, 10))

        pygame.display.flip()

    def check_end(self):
        '''Checks whether goal has been reached'''
        if self.coin_count < Game.max_coins:
            return

        self.game_state['play'] = False
        self.game_state['end'] = True

    def draw_end_screen(self):
        '''Draws the winner screen'''
        if self.player1 > self.player2:
            winner = self.player1
            self.player2.radius = 0
            self.player1.center_pos = [Game.screen_width//2, Game.screen_height//2]
        elif self.player2 > self.player1:
            winner = self.player2
            self.player1.radius = 0
            self.player2.center_pos = [Game.screen_width//2, Game.screen_height//2]
        else:
            winner = choice([self.player1, self.player2])

        self.window.fill(Game.pastel_green)
        
        pygame.draw.circle(self.window, self.player1.color, self.player1.center_pos, self.player1.radius)
        pygame.draw.circle(self.window, self.player2.color, self.player2.center_pos, self.player2.radius)

        p1_points_holder = self.large_font.render(f"{self.player1.points}", False, Game.white) if self.player1.radius != 0 else self.no_font.render(f"{self.player1.points}", False, Game.white)
        p2_points_holder = self.large_font.render(f"{self.player2.points}", False, Game.white) if self.player2.radius != 0 else self.no_font.render(f"{self.player2.points}", False, Game.white)
        self.window.blit(p1_points_holder, (self.player1.center_pos[0]-p1_points_holder.get_width()//2, self.player1.center_pos[1]-p1_points_holder.get_height()//2))
        self.window.blit(p2_points_holder, (self.player2.center_pos[0]-p2_points_holder.get_width()//2, self.player2.center_pos[1]-p2_points_holder.get_height()//2))

        self.window.blit(self.crown, ((Game.screen_width-self.crown_dimen[0])//2, Game.screen_height//2 - winner.radius//2 - self.crown_dimen[1]))

        name_holder = self.large_font.render(f"!!! WINNER !!!", False, Game.black)
        self.window.blit(name_holder, ((Game.screen_width-name_holder.get_width())//2, Game.screen_height//2 + winner.radius + 20))

        pygame.display.flip()

class Player:
    '''A class to define the properties of a player'''

    def __init__(self, pos: list, color: tuple, radius: int, vel: int):
        self.center_pos = list(pos)
        self.color = color
        self.radius = radius
        self.vel = vel
        self.points = 0

    def increase_radius(self, increment: int):
        self.radius += increment

    def move_left(self):
        if 0 <= self.center_pos[0]-self.vel  <= Game.screen_width:
            self.center_pos[0] -= self.vel

    def move_right(self):
        if 0 <= self.center_pos[0]+self.vel  <= Game.screen_width:
            self.center_pos[0] += self.vel

    def move_up(self):
        if 0 <= self.center_pos[1]-self.vel  <= Game.screen_height:
            self.center_pos[1] -= self.vel

    def move_down(self):
        if 0 <= self.center_pos[1]+self.vel  <= Game.screen_height:
            self.center_pos[1] += self.vel

    def add_point(self):
        self.points += 1

    def __lt__(self, another: 'Player'):
        return self.points < another.points
    
    def __gt__(self, another: 'Player'):
        return self.points > another.points

Game().main_loop()