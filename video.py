import cv2
import numpy as np

video_path = 'data/video2.mp4'  # Замените на путь к вашему видеофайлу
window_name = 'OpenCV QR Code'
delay = 1

qcd = cv2.QRCodeDetector()

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Не удалось открыть видеофайл {video_path}")
    exit()

while True:
    ret, frame = cap.read()
    frame1 = frame
    if not ret:
        break  # Выходим из цикла, если видео закончилось

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = cv2.GaussianBlur(frame, (9,9), 0)
    frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    brightness = 10 
    # Adjusts the contrast by scaling the pixel values by 2.3 
    contrast = 2.3  
    frame = cv2.addWeighted(frame, contrast, np.zeros(frame.shape, frame.dtype), 0, brightness) 
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    #frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel, iterations=2)

    ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
    
    if ret_qr:
        for s, p in zip(decoded_info, points):
            if s:
                print(s)
                color = (0, 255, 0)  # Зелёный цвет для успешного декодирования
            else:
                color = (0, 0, 255)  # Красный цвет для неудачного декодирования
            frame1 = frame
            frame = cv2.polylines(frame, [p.astype(int)], True, color, 5)  # Уменьшили толщину линии

    
  
    cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()