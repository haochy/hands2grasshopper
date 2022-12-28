import mediapipe as mp
import cv2
import math
import socket
import queue

def UDP (IP, port,message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(message, "utf-8"),(IP,port))


mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands                    # mediapipe 偵測手掌方法




cap = cv2.VideoCapture(0) 

q = queue.Queue()

IP = "127.0.0.1"
port = 5000

def findHandLandMarks( image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
        results = hands.process(image)
        landMarkList = []

        if results.multi_hand_landmarks:  # returns None if hand is not found
            hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands

            for id, landMark in enumerate(hand.landmark):
                # landMark holds x,y,z ratios of single landmark
                imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([id, xPos, yPos])

            if draw:
                mp_drawing.draw_landmarks(originalImage, hand, mp_hands.HAND_CONNECTIONS)

        return landMarkList



with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    w, h = 540, 310
    while True:
        status, image = cap.read()
        image = cv2.resize(image, (w,h))
        image = cv2.flip(image, 1)
        handLandmarks = findHandLandMarks(image=image, draw=True)
        # prev_length = 0
        if(len(handLandmarks) != 0):
            x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
            x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
            # if (q.qsize() <= 10):
            #     q.put(x1,y1,x2,y2)
            # else:
            #     q.get()
            #     q.put(x1,y1,x2,y2)
            #     sum = 0
            #     for i in list(q.queue):
            #         sum += i
            length = math.hypot(x2-x1, y2-y1)
            middlex = (x1+x2)/2
            middley = (y1+y2)/2 
                
            message = "{},{},{},{},{}".format(w,h,length,middlex,middley)
            # print(message)

            UDP(IP, port, message)
            prev_length = length


        cv2.imshow("UDP2grasshopper", image)
        cv2.waitKey(1)