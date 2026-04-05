
from picamera2 import Picamera2
import cv2
import RPi.GPIO as GPIO
import time
from hand_detector_led_control import handDetection

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

LED_PIN0= 18
LED_PIN1= 23
LED_PIN2= 25
LED_PIN3= 24
LED_PIN4= 27

GPIO.setup(LED_PIN0, GPIO.OUT)
GPIO.setup(LED_PIN1, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(LED_PIN3, GPIO.OUT)
GPIO.setup(LED_PIN4, GPIO.OUT)


detection = handDetection()
try:
    while True:

        frame = picam2.capture_array()
        detection.handDetect(frame)
        counter = detection.fingerCounter()
        cv2.imshow("Pi Camera (Bullseye)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if counter ==0:
            GPIO.output(LED_PIN0, GPIO.HIGH)
            print("LED ON")
            time.sleep(1)

        elif counter == 1:
            GPIO.output(LED_PIN1, GPIO.HIGH)
            print("LED ON")
            time.sleep(1)

        elif counter == 2:
            GPIO.output(LED_PIN2, GPIO.HIGH)
            print("LED ON")
            time.sleep(1)

        elif counter == 3:
            GPIO.output(LED_PIN3, GPIO.HIGH)
            print("LED ON")
            time.sleep(1)

        elif counter == 4:
            GPIO.output(LED_PIN4, GPIO.HIGH)
            print("LED ON")
            time.sleep(1)
        else:

            GPIO.output(LED_PIN0, GPIO.LOW)
            GPIO.output(LED_PIN1, GPIO.LOW)
            GPIO.output(LED_PIN2, GPIO.LOW)
            GPIO.output(LED_PIN3, GPIO.LOW)
            GPIO.output(LED_PIN4, GPIO.LOW)
            print("LED OFF")
            time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()

cv2.destroyAllWindows()