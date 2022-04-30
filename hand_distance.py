from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.7, maxHands=1)

def calculate(img):
    hands = detector.findHands(img, draw=False)

    if hands:
        lmList = hands[0]['lmList']
        x1, y1, z1 = lmList[5]
        x2, y2, z2 = lmList[17]
        distance = int(((y2 - y1)**2 + (x2-x1)**2)**(1/2))
        return round(4500/distance, 2)
    return False
