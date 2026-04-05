import mediapipe as mp
import cv2
import time
import math


class handDetection:

    def __init__(self):

        self.myHands = mp.solutions.hands
        self.hands = self.myHands.Hands()
        self.drawLandMarks = mp.solutions.drawing_utils

        self. current_Time = 0
        self.present_Time = 0

        self.top_points = [4, 8, 12, 16, 20]
        self.mid_points = [3, 6, 10, 14, 18]

        self.total_points=[]
        self.fingers = []

    def hand_draw(self,frame):
        global fingersCount
        while True:
            frame = cv2.flip(frame,1)
            RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.current_Time = time.time()
            fps = 1 / (self.current_Time - self.present_Time)
            self.present_Time = self.current_Time

            cv2.putText(frame, str(int(fps)), (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            results = self.hands.process(RGB_image)

            if results.multi_hand_landmarks:
                total_points = []  # Reset Frame
                fingers = [] #Reset Frame
                for handLMS in results.multi_hand_landmarks:
                  for id,lms in enumerate(handLMS.landmark):
                      h,w,c=frame.shape
                      tw ,th = int((lms.x*w)) , int((lms.y*h))

                      total_points.append([tw,th])

                  self.drawLandMarks.draw_landmarks(frame,handLMS,self.myHands.HAND_CONNECTIONS)

                cv2.rectangle(frame, (40, 70), (100, 200), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, str(int(fingersCount)), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        self.video.release()
        cv2.destroyAllWindows()

                    #Thumb
    def fingerCounter(self):
      if self.total_points[4][0] < self.total_points[3][0]:
        self.fingers.append(1)  # Open

      else:
        self.fingers.append(0)  # Closed


    # Others fingers
      for i in range(1,5):
         if self.total_points[self.top_points[i]][1] < self.total_points[self.mid_points[i]][1]:
            self.fingers.append(1)
         else:
            self.fingers.append(0)

      fingersCount = self.fingers.count(1)

      return fingersCount



if __name__ == "__main__":
    obj = handDetection()
    obj.hand_draw(frame)