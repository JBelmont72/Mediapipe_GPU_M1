import cv2
import mediapipe as mp
import tensorflow as tf
## instructions to load tensor flow below
# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Start capturing video
cap = cv2.VideoCapture(1)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the BGR image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image with Mediapipe
    results = hands.process(image)

    # Draw the hand annotations on the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the image
    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(1) & 0xFF == 27:  # Esc key to exit
        break

cap.release()
cv2.destroyAllWindows()

'''
https://www.youtube.com/watch?v=F8gxBAgAk58


https://www.youtube.com/watch?v=F8gxBAgAk58

www.codegive.com. for media pipe on m1 macOS to use GPU

Install TensorFlow with the following command:

```bash
pip install tensorflow-macos tensorflow-metal
```

This command installs TensorFlow optimized for macOS and supports Metal, which allows GPU acceleration on Apple silicon.

### Step 5: Install Mediapipe

Now, you can install the Mediapipe library. Run the following command:

```bash
pip install mediapipe
```

### Step 6: Verify Installation

You can verify that both TensorFlow and Mediapipe are installed correctly by running:

```python
import tensorflow as tf
import mediapipe as mp

print("TensorFlow version:", tf.__version__)
print("Mediapipe version:", mp.__version__)
```

If you see the versions printed without any errors, the installation was successful.

'''