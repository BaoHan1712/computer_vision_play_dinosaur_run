import cv2 
import time
import mediapipe as mp
import pyautogui

cap =cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime =0
cTime =0

down_held = False 
start_hold_time = None  
space_held = False
start_space_time = None

while True:
    success,img=cap.read()
    imRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imRGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in handLms.landmark]
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
        # chạm để nhảy
        thumb_tip1, index_tip1 = lmList[4], lmList[8]
        distance1 = ((thumb_tip1[0] - index_tip1[0]) ** 2 + (thumb_tip1[1] - index_tip1[1]) ** 2) ** 0.5
        thumb_tip2, index_tip2 = lmList[4], lmList[12]
        distance2 = ((thumb_tip2[0] - index_tip2[0]) ** 2 + (thumb_tip2[1] - index_tip2[1]) ** 2) ** 0.5
    
        if distance1 < 25:
            if not space_held:  # Chỉ nhấn khi space chưa được giữ
                pyautogui.press('space')
                space_held = True
                start_space_time = time.time()
                print("đang nhấn space")
        else:
            if space_held:
                space_held = False
                start_space_time = None

  # giữ phím down          
        if distance2 < 25:
            if not down_held:
                pyautogui.keyDown('down')
                start_hold_time = time.time()
                down_held = True
                print("Phím down đang giữ")
        else:
            if down_held:
                pyautogui.keyUp('down')
                down_held = False
                start_hold_time = None

    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
      
    cv2.imshow("Runtime", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
