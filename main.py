import cv2
import mediapipe as mp
import pyautogui
import keyboard

video = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils


def cam_Size2monitor_Size(cam_width, cam_height, x, y):
    screenWidth, screenHeight = pyautogui.size()

    width_proportion = screenWidth / cam_width
    height_proportion = screenHeight / cam_height

    return y*height_proportion, x*width_proportion


while True:
    ret, image = video.read()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                    print(f"x: {cx}, y: {cy}")

                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        try:
            pyautogui.moveTo(cam_Size2monitor_Size(h, w, cx, cy))
        except:
            pass

    if keyboard.is_pressed("a"):
        break

    cv2.imshow("Output", image)
    cv2.waitKey(1)
