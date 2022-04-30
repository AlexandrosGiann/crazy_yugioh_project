from cvzone.FaceMeshModule import FaceMeshDetector

detector = FaceMeshDetector(maxFaces=1)

def calculate(img):
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3
        f = 755
        d = (W*f)/w
        return round(d, 2)
    return False
