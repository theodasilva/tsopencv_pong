#!/usr/bin/env python3

import sys
import time
import random
import pygame
import cv2
import numpy as np
from vision import camera
from fist import fist_pos
from pygame.locals import *
from threading import Thread
from vision import information

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# globals
WIDTH = 1100
HEIGHT = 700
BALL_SIZE = 10
BALL_SPEED = 1.4
paddle1_vel = 0
paddle2_vel = 0
PAD_WIDTH = 15
PAD_HEIGHT = 100
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
IA = True

class Game(Thread):
    def __init__(self, info):
        Thread.__init__(self)
        self.info = info

    def run(self):
        init(info)
        game_loop(self.info)

def start_ball(side):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)
    if side == False:
        horz = -horz
    ball_vel = [horz, -vert]

def init(info):
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score
    paddle1_pos = [PAD_WIDTH / 2 - 1,HEIGHT / 2]
    paddle2_pos = [WIDTH + 1 - PAD_WIDTH / 2, HEIGHT / 2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        start_ball(True)
    else:
        start_ball(False)
    # calibrage(info)

def pong(window, info):
    global paddle1_pos, paddle1_vel, paddle2_pos, ball_pos, ball_vel, l_score, r_score, IA

    # basic AI
    if IA == True:
        if paddle1_pos[1] > ball_pos[1]:
            paddle1_vel = -6
        else:
            paddle1_vel = 6

    if paddle1_pos[1] > PAD_HEIGHT / 2 and paddle1_pos[1] < HEIGHT - PAD_HEIGHT / 2:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == PAD_HEIGHT / 2 and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - PAD_HEIGHT / 2 and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    # update paddle 2
    paddle2_pos[1] = info.hand * HEIGHT / 100

    # update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    # ball collison on wall
    if int(ball_pos[1]) <= BALL_SIZE:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_SIZE:
        ball_vel[1] = -ball_vel[1]

    # ball collison on sides
    if int(ball_pos[0]) <= BALL_SIZE + PAD_WIDTH and int(ball_pos[1]) in range(int(paddle1_pos[1] - PAD_HEIGHT / 2), int(paddle1_pos[1] + PAD_HEIGHT / 2), 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= BALL_SPEED
        ball_vel[1] *= BALL_SPEED
    elif int(ball_pos[0]) <= BALL_SIZE + PAD_WIDTH:
        r_score += 1
        start_ball(True)
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_SIZE - PAD_WIDTH and int(ball_pos[1]) in range(int(paddle2_pos[1] - PAD_HEIGHT / 2), int(paddle2_pos[1] + PAD_HEIGHT / 2), 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= BALL_SPEED
        ball_vel[1] *= BALL_SPEED
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_SIZE - PAD_WIDTH:
        l_score += 1
        start_ball(False)

    # draw ball
    ball_pos[0] = int(ball_pos[0])
    ball_pos[1] = int(ball_pos[1])
    pygame.draw.circle(window, WHITE, ball_pos, BALL_SIZE, 0)

    # draw players
    pygame.draw.polygon(window, WHITE, [[paddle1_pos[0] - PAD_WIDTH / 2, paddle1_pos[1] - PAD_HEIGHT / 2], [paddle1_pos[0] - PAD_WIDTH / 2, paddle1_pos[1] + PAD_HEIGHT / 2], [paddle1_pos[0] + PAD_WIDTH / 2, paddle1_pos[1] + PAD_HEIGHT / 2], [paddle1_pos[0] + PAD_WIDTH / 2, paddle1_pos[1] - PAD_HEIGHT / 2]], 0)
    pygame.draw.polygon(window, WHITE, [[paddle2_pos[0] - PAD_WIDTH / 2, paddle2_pos[1] - PAD_HEIGHT / 2], [paddle2_pos[0] - PAD_WIDTH / 2, paddle2_pos[1] + PAD_HEIGHT / 2], [paddle2_pos[0] + PAD_WIDTH / 2, paddle2_pos[1] + PAD_HEIGHT / 2], [paddle2_pos[0] + PAD_WIDTH / 2, paddle2_pos[1] - PAD_HEIGHT / 2]], 0)

    # draw score
    myfont1 = pygame.font.SysFont("Britannic Bold", 100)
    scoreP1 = myfont1.render(str(l_score), 1, (255,255,255))
    window.blit(scoreP1, (WIDTH / 2 - 100,20))
    myfont2 = pygame.font.SysFont("Britannic Bold", 100)
    scoreP2 = myfont2.render(str(r_score), 1, (255,255,255))
    window.blit(scoreP2, (WIDTH / 2 + 62, 20))

    # draw game lines
    i = 12
    while i < 1000:
        pygame.draw.line(window, WHITE, [WIDTH / 2, i],[WIDTH / 2, i + 25], 1)
        i += 50
    pygame.draw.line(window, WHITE, [0, 0],[WIDTH, 0], 1)
    pygame.draw.line(window, WHITE, [0, HEIGHT - 1],[WIDTH, HEIGHT - 1], 1)

def key_down(event):
    global paddle1_vel, paddle2_vel, IA, paddle1_pos
    if event.key == K_z:
        IA = False
        paddle1_vel = -2
    elif event.key == K_s:
        IA = False
        paddle1_vel = 2

def key_up(event):
    global paddle1_vel, paddle2_vel
    if event.key in (K_z, K_s):
        paddle1_vel = 0

def game_loop(info):
    global l_score, r_score
    pygame.init()
    pygame.display.set_caption('Pong 2k18')
    fps = pygame.time.Clock()
    init(info)

    info.frame = False
    print("Calibrage haut")
    time.sleep(3)
    h = fist_pos(info)
    print(h)
    print("Calibrage bas" )
    time.sleep(3)
    b = fist_pos(info)
    print(b)
    info.f_calibrage = True
    info.calibrage_max = b[0][1] - h[0][1]

    while True:
        if l_score > 9 or r_score > 9:
            pygame.quit()
            sys.exit()
        window.fill(BLACK)
        pong(window, info)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                key_down(event)
            elif event.type == KEYUP:
                key_up(event)
        pygame.display.update()
        fps.tick(100)

if __name__ == "__main__":
    info = information
    cam = camera(info)
    game = Game(info)
    cam.start()
    game.start()
    cam.join()
    game.join()
