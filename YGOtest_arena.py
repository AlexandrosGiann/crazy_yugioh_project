import cv2
import os
import numpy as np
import cvzone
import pygame
pygame.init()

wn = pygame.display.set_mode((625, 400), pygame.RESIZABLE)

pygame.display.set_caption('')

def overlay(img, bg, x=100, y=100):
    return cvzone.overlayPNG(bg, img, [x, y])

def transform(img, looking_at='left'):
    rows,cols,ch = img.shape
    pts1 = np.float32([[0,0],[200, 0],[200,300],[0,300]])
    if looking_at == 'left':
        pts2 = np.float32([[25,0],[150,25],[150,275],[25,300]])
    elif looking_at == 'right':
        pts2 = np.float32([[50,25],[175,0],[175,300],[50,275]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(300,300))
    return dst

width = wn.get_width()
height = wn.get_height()

run = True

while run:
    pygame.time.delay(10)

    img = cv2.imread('blue_futuristic_background3.jpg')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    c = 0
    c1 = 0
    w = 50
    h = 120
    for card in os.listdir('CARD_DB/spell_cards')[:5]:
        img1 = cv2.imread(f'CARD_DB/spell_cards/{card}')
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2BGRA)
        img1 = transform(img1)
        img1 = img1[0 : 300, 25 : 150]
        img1 = cv2.resize(img1, (w, h), interpolation = cv2.INTER_AREA)
        img = overlay(img1, img, 40 + c,  160 + c1)
        w -= 5
        v1 = round(round(25/90 * h)* 2/3)
        h -= v1
        c += w + 10
        c1 += v1//2
    w += 5
    h += v1
    c = 0
    c1 -= v1//2
    for card in os.listdir('CARD_DB/spell_cards')[:5]:
        img1 = cv2.imread(f'CARD_DB/spell_cards/{card}')
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2BGRA)
        img1 = transform(img1, 'right')
        img1 = img1[0 : 300, 50 : 175]
        img1 = cv2.resize(img1, (w, h), interpolation = cv2.INTER_AREA)
        img = overlay(img1, img, 353 + c,  160 + c1)
        w += 5
        v1 = round(round(25/90 * h)* 2/3)
        h += v1
        c += w
        c1 -= v1//2
    wn.fill((0, 0, 60))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = pygame.image.frombuffer(img, img.shape[1::-1], 'RGB')
    wn.blit(img, (0, 0))
    pygame.draw.rect(wn, (255, 0, 0), (311, 0, 3, 480))
    pygame.display.update()
pygame.quit()
