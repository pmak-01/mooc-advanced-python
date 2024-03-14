from random import randint

import pygame
pygame.init()

clock = pygame.time.Clock()
game_font = pygame.font.SysFont("Arial", 24)

screen_width, screen_height = 640, 480
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Asteriods')
window.fill((0,0,0))

robot = pygame.image.load('src/robot.png')
robot_width, robot_height = robot.get_width(), robot.get_height()
robot_pos = [0, screen_height-robot_height]
robot_flags = [False, False]

rock = pygame.image.load('src/rock.png')
rock_width, rock_height = rock.get_width(), rock.get_height()
rock_positions = []
points = 0
c = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                robot_flags[0] = True
            if event.key == pygame.K_RIGHT:
                robot_flags[1] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                robot_flags[0] = False
            if event.key == pygame.K_RIGHT:
                robot_flags[1] = False

    # Rock logic
    c += 1
    c %= 200
    if not c%40:
        rock_positions.append([randint(0, screen_width-rock_width), 0])

    to_remove = []
    for i in range(len(rock_positions)):
        rock_positions[i][1] += 2
        
        if rock_positions[i][1] + rock_height > screen_height:
            print(f"\nOh no, an asteriod hit! You earned {points} points\n")
            exit()
            #to_remove.append(rock_positions[i])
    # Rock logic end
        
    # Robot logic start
    if 0 <= robot_pos[0]-10 and robot_flags[0]:
        robot_pos[0] -= 10
    if robot_pos[0]+10 <= screen_width-robot_width and robot_flags[1]:
        robot_pos[0] += 10
    # Robot logic end
        
    # Points logic start
    for rock_pos in rock_positions:
        x_inrange = rock_pos[0] in range(robot_pos[0], robot_pos[0]+robot_width+1) or rock_pos[0]+rock_width in range(robot_pos[0], robot_pos[0]+robot_width+1)
        y_inrange = rock_pos[1] in range(robot_pos[1], robot_pos[1]+robot_height+1) or rock_pos[1]+rock_height in range(robot_pos[1], robot_pos[1]+robot_height+1)
        if x_inrange and y_inrange:
            points += 1
            #print(f"Yay! you gained a point! Now your points are {points}")
            to_remove.append(rock_pos)
    # Points logic end

    for pos in to_remove:
        if pos in rock_positions:
            rock_positions.remove(pos)

    # Display code start
    points_text = game_font.render(f"Points: {points}", False, (255,0,0))
    window.fill((0,0,0))
    for pos in rock_positions:
        window.blit(rock, pos)
    window.blit(robot, robot_pos)
    window.blit(points_text, (screen_width-points_text.get_width(), 0))
    # Display code end

    clock.tick(60)
    pygame.display.flip()