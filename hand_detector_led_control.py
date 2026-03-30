import mediapipe as mp
import cv2
import time
import math

top_points=[4,8,12,16,20]
mid_points=[3,6,10,14,18]

total_points=[]
fingers=[]

myHands = mp.solutions.hands
hands =myHands.Hands()
drawLandMarks = mp.solutions.drawing_utils

current_Time = 0
present_Time = 0
video = cv2.VideoCapture(0)

x4=y4=x8=y8=x0=y0=x12=y12=x16=y16=x20=y20 =0

while True:
    success, frame = video.read()
    frame = cv2.flip(frame,1)
    RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if not success:
         print("Failed to receive a frame")
         continue

    results = hands.process(RGB_image)
    # global distance4,distance8,distance12,distance16,distance20

    if results.multi_hand_landmarks:
        total_points = []  # Reset Frame
        fingers = [] #Reset Frame
        for handLMS in results.multi_hand_landmarks:
          for id,lms in enumerate(handLMS.landmark):
              h,w,c=frame.shape
              tw ,th = int((lms.x*w)) , int((lms.y*h))

              total_points.append([tw,th])



          drawLandMarks.draw_landmarks(frame,handLMS,myHands.HAND_CONNECTIONS)

            #Thumb Case
          if total_points[4][0] > total_points[3][0]:
                fingers.append(1)  # Open
                print("Open")
          else:
                fingers.append(0)  # Closed
                print("Close")

            # Others fingers
          for i in range(1,5):
            if total_points[top_points[i]][1] < total_points[mid_points[i]][1]:
                    fingers.append(1)
            else:
                    fingers.append(0)

        if fingers == [1, 0, 0, 0, 0]:
            print("1 → Thumb")

        elif fingers == [0, 1, 0, 0, 0]:
            print("2 → Index")

        elif fingers == [0, 0, 1, 0, 0]:
            print("3 → Middle")

        elif fingers == [0, 0, 0, 1, 0]:
            print("4 → Ring")

        elif fingers == [0, 0, 0, 0, 1]:
            print("5 → Pinky")


    current_Time  = time.time()
    fps = 1/(current_Time - present_Time)
    present_Time = current_Time

    cv2.putText(frame, str(int(fps)), (40, 80),cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)
    cv2.imshow("Frame",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

