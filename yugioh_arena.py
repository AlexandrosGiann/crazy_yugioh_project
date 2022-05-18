import os
import cv2
import numpy as np
import face_distance
import hand_distance
import speech_recognition as sr
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import pygame
pygame.init()

wn = pygame.display.set_mode((1000, 480), pygame.RESIZABLE)
pygame.display.set_caption('')

width = wn.get_width()
height = wn.get_height()

def get_speech():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            return text.lower()
    except:
        return False

def overlay(img, bg):
    return cvzone.overlayPNG(bg, img, [100, 100])

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

class Arena:
    def __init__(self):
        self.monster_zone = []
        self.spell_and_trap_zone = []
        self.spell_and_trap_zone1 = []

    def visualize_spell_and_trap_zone(self, img):
        c = 0
        c1 = 0
        w = 50
        h = 120
        for card in os.listdir(self.spell_and_trap_zone):
            img1 = cv2.imread(f'CARD_DB/{card}')
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
        for card in os.listdir(self.spell_and_trap_zone1):
            img1 = cv2.imread(f'CARD_DB/{card}')
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
        return img

cap = cv2.VideoCapture(0)
segmentor = SelfiSegmentation()
lst = [line.split() for line in open("CARD_IDS.txt", 'r').readlines()]
run = True
appear_mode = 0

FONT = pygame.font.SysFont('Consolas', 16)

indexes = [0, 25, 22, 24, 20, 19, 32, 26, 35, 23, 27, 21, 33, 28, 31, 30, 34, 29, 14, 11, 17, 12, 13, 10, 16, 3, 9, 5, 18, 8, 15, 1, 2, 6, 4, 7]

while run:
    pygame.time.delay(10)

    _, img = cap.read()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    wn.fill((0, 0, 60))
    
    TEXT1 = FONT.render('Face Distance: ' + str(face_distance.calculate(img)), True, (0, 255, 255))
    TEXT2 = FONT.render('Hand Distance: ' + str(hand_distance.calculate(img)), True, (0, 255, 255))
    wn.blit(TEXT1, (645, 446))
    wn.blit(TEXT2, (645, 463))
    img1 = img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], 'RGB')
    wn.blit(img, (0, 0))
    code = open('game_data.txt', 'r').read()
    l = 0
    for l in lst:
        if code == l[0]:
            text = l[1].lower()
            if f'rsz_{text}_card.jpg' in os.listdir('CARD_DB/extra_deck_cards'):
                card_image = pygame.image.load(f'CARD_DB/extra_deck_cards/rsz_{text}_card.jpg')
                monster_image = pygame.image.load(f'CARD_DB/extra_deck_monsters/{text}_transparent.png')
                wn.blit(card_image, (700, 100))
                wn.blit(monster_image, (200, 100))
                appear_mode = 1
            elif f'rsz_{text}_CARD.jpg' in os.listdir('CARD_DB/main_deck_monster_cards'):
                card_image = pygame.image.load(f'CARD_DB/main_deck_monster_cards/rsz_{text}_CARD.jpg')
                monster_image = pygame.image.load(f'CARD_DB/main_deck_monsters/{text}_transparent.png')
                wn.blit(card_image, (700, 100))
                wn.blit(monster_image, (200, 100))
                appear_mode = 1
            elif f'rsz_{text}_card.jpg' in os.listdir('CARD_DB/spell_cards'):
                card_image = pygame.image.load(f'CARD_DB/spell_cards/rsz_{text}_card.jpg')
                wn.blit(card_image, (700, 100))
                card_image1 = cv2.imread(f'CARD_DB/spell_cards/rsz_{text}_card.jpg')
                appear_mode = 2
            elif f'rsz_{text}_card.jpg' in os.listdir('CARD_DB/trap_cards'):
                card_image = pygame.image.load(f'CARD_DB/trap_cards/rsz_{text}_card.jpg')
                card_image1 = cv2.imread(f'CARD_DB/trap_cards/rsz_{text}_card.jpg')
                wn.blit(card_image, (700, 100))
                appear_mode = 2
            break
    if appear_mode == 1:
        wn1 = pygame.surfarray.array3d(wn)[0: 640]
        wn1 = cv2.cvtColor(wn1, cv2.COLOR_RGB2BGR)
        wn1 = cv2.rotate(wn1, 2)[::-1]
        imgOUT = segmentor.removeBG(img1, wn1, 0.7)
        imgOUT = cv2.cvtColor(imgOUT, cv2.COLOR_BGR2RGB)
        imgOUT = pygame.image.frombuffer(imgOUT.tobytes(), imgOUT.shape[1:: -1], "RGB")
        wn.blit(imgOUT, (0, 0))
    elif appear_mode == 2:
        card_image1 = cv2.cvtColor(card_image1, cv2.COLOR_BGR2BGRA)
        card_image1 = transform(card_image1)
        imgOUT = overlay(card_image1, img1)
        imgOUT = segmentor.removeBG(img1, imgOUT, 0.7)
        imgOUT = cv2.cvtColor(imgOUT, cv2.COLOR_BGR2RGB)
        imgOUT = pygame.image.frombuffer(imgOUT.tobytes(), imgOUT.shape[1:: -1], "RGB")
        wn.blit(imgOUT, (0, 0))
    pygame.display.update()
cap.release()
pygame.quit()
