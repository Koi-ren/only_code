import cv2
import numpy as np

# 카메라 연결
cap = cv2.VideoCapture('C:/Users/plane/Advanced-lane-finding/challenge_video.mp4')

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    # 이미지를 회색으로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Canny 엣지 검출
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # 선분 검출
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        # 중앙에서 가장 가까운 선 찾기
        center_x = frame.shape[1] // 2
        closest_line = None
        closest_distance = float('inf')
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            line_center_x = (x1 + x2) // 2
            distance = abs(line_center_x - center_x)
            if distance < closest_distance:
                closest_line = line
                closest_distance = distance
        
        if closest_line is not None:
            # 가장 가까운 선 그리기
            x1, y1, x2, y2 = closest_line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, frame.shape[0] // 2), 5, (0, 0, 255), -1)
    
    # 화면에 출력
    cv2.imshow('frame', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
