import cv2

webcam = cv2.VideoCapture(0)
fps = webcam.get(cv2.CAP_PROP_FPS)
print('fps:', fps)

ret, frame = webcam.read()
img = frame.copy()

height = img.shape[0]
width = img.shape[1]

roi_size = 200
roi_x1 = int(width/2 - roi_size/2)
roi_y1 = int(height/2 - roi_size/2)
roi_x2 = int(roi_x1 + roi_size)
roi_y2 = int(roi_y1 + roi_size)
green = (0, 255, 0)
thick = 15

tracker = cv2.legacy.TrackerCSRT()
roi = (roi_x1, roi_y1, roi_x2-roi_x1, roi_y2 - roi_y1)
print('RI x, y, w, h: ', +roi[0])
tracker.init(frame, roi)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()
    isFound, foundBox = tracker.update(frame)

    if status:
        found_x1 = int(foundBox[0])
        found_y1 = int(foundBox[1])
        found_x2 = int(foundBox[0] + foundBox[2])
        found_y2 = int(foundBox[1] + foundBox[3])

        cv2.rectangle(frame, (found_x1, found_y1),(found_x2, found_y2), green, thick)

        cv2.imshow("test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()