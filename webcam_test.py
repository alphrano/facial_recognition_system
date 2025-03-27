import cv2

cap = cv2.VideoCapture(0)  # Open the webcam

while True:
    ret, frame = cap.read()  # Read frame
    if not ret:
        print("Error: Couldn't access webcam")
        break

    cv2.imshow("Webcam Test - Press 'q' to Exit", frame)  # Show webcam feed

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
