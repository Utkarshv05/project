import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize Mediapipe components
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Dictionary for label mapping
labels_dict = {i: chr(65 + i) for i in range(26)}  # Generates A-Z mapping

# Buffer to store detected characters
text_buffer = ""
predicted_character = None  # To hold the current predicted character
stable_prediction_count = 0  # Counter for stable predictions
stable_threshold = 5  # Number of frames to confirm a stable prediction

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Flip the video frame horizontally
    frame = cv2.flip(frame, 1)

    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        # Process only the first detected hand
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )

        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y

            x_.append(x)
            y_.append(y)

        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y
            data_aux.append(x - min(x_))
            data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Predict the character using the model
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character_new = labels_dict[int(prediction[0])]

         # Check if we have a new stable prediction or not
        if predicted_character == predicted_character_new:
            stable_prediction_count += 1  # Increment stable count if same character is detected
            
            # If stable prediction count exceeds threshold, update text buffer
            if stable_prediction_count >= stable_threshold:
                if len(text_buffer) == 0:
                    text_buffer += predicted_character_new
                    stable_threshold = 5
                    stable_prediction_count = 0
                elif predicted_character != text_buffer[-1]:
                    text_buffer += predicted_character_new
                    #print(text_buffer[-1])
                    stable_threshold = 5
                    stable_prediction_count = 0
                elif predicted_character == text_buffer[-1] and stable_threshold == 5:
                    stable_threshold = 10
                    stable_prediction_count = 0
                elif stable_prediction_count >= stable_threshold and predicted_character == text_buffer[-1]:
                    text_buffer += predicted_character_new
                    stable_threshold = 5
                    stable_prediction_count = 0
        else:
            stable_prediction_count = 0  # Reset count if different character detected


        predicted_character = predicted_character_new  # Update current prediction

        # Display the bounding box and detected letter (without confidence score)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        if predicted_character is not None:
            cv2.putText(frame, predicted_character, 
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

    # Display the accumulated text on the frame
    cv2.putText(frame, f"Text: {text_buffer}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                (255, 0, 0), 3, cv2.LINE_AA)

    # Show the frame
    cv2.imshow('Sign Language Interpreter', frame)

    # Key controls
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):  # Quit the program
        break
    elif key == ord('c'):  # Clear the text buffer
        text_buffer = ""
        predicted_character = None
    elif key == ord(' '):  # Add space to text buffer on spacebar press
        text_buffer += " "  

cap.release()
cv2.destroyAllWindows()