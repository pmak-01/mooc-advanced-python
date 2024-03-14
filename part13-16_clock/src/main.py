from math import sin, cos, pi
import datetime

import pygame
pygame.init()

window = pygame.display.set_mode((1240, 640))
window.fill((0,0,0))

sec_angle, min_angle, hr_angle = 0,0,0
len_sec, len_min, len_hr = 200, 200, 140
width_sec, width_min, width_hr = 2, 3, 4
clock_radius, clock_thickness = 220, 5
center = (1240//2, 640//2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    window.fill((0,0,0))

    curr = datetime.datetime.now()
    hr, min, sec = curr.hour, curr.minute, curr.second
    pygame.display.set_caption(f"{hr//10}{hr%10}:{min//10}{min%10}:{sec//10}{sec%10}")

    pygame.draw.circle(window, (255,0,0), center, clock_radius)
    pygame.draw.circle(window, (0,0,0), center, clock_radius-clock_thickness)
    pygame.draw.circle(window, (255,0,0), center, 10)

    sec_angle = sec/60 * 2*pi
    sec_pos = (620 - len_sec*cos(sec_angle+pi/2), 320 - len_sec*sin(sec_angle+pi/2))
    min_angle = (min + sec/60)/60 * 2*pi
    min_pos = (620 - len_min*cos(min_angle+pi/2), 320 - len_min*sin(min_angle+pi/2))
    hr_angle = (hr%12 + min/60 + sec/3600)/12 * 2*pi
    hr_pos = (620 - len_hr*cos(hr_angle+pi/2), 320 - len_hr*sin(hr_angle+pi/2))

    pygame.draw.line(window, (0,0,255), center, sec_pos, width=width_sec)
    pygame.draw.line(window, (0,0,255), center, min_pos, width=width_min)
    pygame.draw.line(window, (0,0,255), center, hr_pos, width=width_hr)

    pygame.display.flip()