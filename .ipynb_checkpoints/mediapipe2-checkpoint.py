import mediapipe as mp
import cv2
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

class Rectangle:
    def __init__(self, x, y, w, h, row, column):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.row = row
        self.column = column
        self.color = (0, 255, 0) 
        self.alpha = 100

    def click_action(self, frame):
        if self.row == 2 and self.column == 3:
            cv2.putText(frame, "Right", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        elif self.row == 1 and self.column == 2:
            cv2.putText(frame, "up", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        elif self.row == 3 and self.column == 2:
            cv2.putText(frame, "down", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        elif self.row == 2 and self.column == 2:
            cv2.putText(frame, "stop", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        elif self.row == 2 and self.column == 1:
            cv2.putText(frame, "Left", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, f"{self.row}row {self.column}column", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        overlay = frame.copy()
        cv2.rectangle(overlay, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 255, 255), -2)
        cv2.addWeighted(overlay, self.alpha / 255, frame, 1 - self.alpha / 255, 0, frame)

    def update_color(self, color):
        self.color = color

rectangles = []
for i in range(3):
    for j in range(3):
        x = j * 110 + 100
        y = i * 110 + 100
        rectangles.append(Rectangle(x, y, 100, 100, i + 1, j + 1))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            finger_tip_x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            finger_tip_y = int(hand_landmarks.landmark[8].y * frame.shape[0])

            for rect in rectangles:
                if rect.x < finger_tip_x < rect.x + rect.w and rect.y < finger_tip_y < rect.y + rect.h:
                    rect.click_action(frame)
                    rect.update_color((0, 0, 255)) 
                else:
                    rect.update_color((0, 255, 0))
                    rect.alpha = 100 

    for rect in rectangles:
        cv2.rectangle(frame, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), rect.color, 2)

    cv2.imshow('Transparent Rectangles', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()