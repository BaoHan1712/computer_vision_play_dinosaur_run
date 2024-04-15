import cv2 
import time
import mediapipe as mp
import pyautogui

cap =cv2.VideoCapture(0)
mpHands = mp.solutions.hands
# phát hiện tay
hands = mpHands.Hands()
# vẽ lại các khớp tay
mpDraw = mp.solutions.drawing_utils
# tính FPS
pTime =0
cTime =0

# giữ phím Down Arrow
down_held = False 
# Bắt đầu giữ phím
start_hold_time = None  
while True:
    success,img=cap.read()
    # chuyển màu từ BGR sang RGB
    imRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # xử lý ảnh để phát hiện bàn tay
    results = hands.process(imRGB)
    
    if results.multi_hand_landmarks:
    # duyệt qua từng ngón tay
        for handLms in results.multi_hand_landmarks:
            lmList = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in handLms.landmark]
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
        # chạm để nhảy
        thumb_tip1, index_tip1 = lmList[4], lmList[8]
        distance1 = ((thumb_tip1[0] - index_tip1[0]) ** 2 + (thumb_tip1[1] - index_tip1[1]) ** 2) ** 0.5
        thumb_tip2, index_tip2 = lmList[4], lmList[12]
        distance2 = ((thumb_tip2[0] - index_tip2[0]) ** 2 + (thumb_tip2[1] - index_tip2[1]) ** 2) ** 0.5
    
# nếu khoảng cách nhỏ hơn 40 thì .....
        if distance1 < 45:
            pyautogui.press('space') 
            # start_time = time.time()
            print("đang chạm nút space nè")
            
  # giữ phím down          
        if distance2 < 45:
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
                
#thời gian thực và ghi ra
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
      
    cv2.imshow("Runtime", img)
    
    # Thoát khỏi vòng lặp 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
