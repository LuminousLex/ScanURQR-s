import cv2
from qreader import QReader
import warnings
import threading
import time
from tkinter.filedialog import asksaveasfilename
from imutils.video import VideoStream

# Глобальные события для управления потоком
stop_event = threading.Event()
pause_event = threading.Event()


def bbox_show(frame, point1: tuple[int, int], point2: tuple[int, int], name: str | None, is_valid: bool) -> None:
    """Отрисовка QR-code и рамки"""
    text = ('None' if name is None else name)
    point_text = (point1[0], point1[1] - 10)
    color = (0, 0, 255) if not is_valid else (0, 255, 0)
    
    frame = cv2.putText(img=frame, text=text, org=point_text,
                       fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, 
                       color=color, thickness=3)
    frame = cv2.rectangle(frame, point1, point2, color, 2)


def reset_events():
    """Сбросить все события перед новым запуском"""
    global stop_event, pause_event
    stop_event.clear()
    pause_event.clear()


def toggle_pause():
    """Переключить состояние паузы"""
    if pause_event.is_set():
        pause_event.clear()
    else:
        pause_event.set()


def set_stop():
    """Принудительная остановка потока"""
    stop_event.set()


def is_paused():
    """Проверить, стоит ли пауза"""
    return pause_event.is_set()


def _check_window_close(window_name: str) -> bool:
    """Безопасная проверка закрытия окна через крестик"""
    try:
        return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1
    except Exception:
        return False


def camera_scanning(valid_text: list, skip_frame: int, PredProc: int, filter_warnings: bool=True) -> set:
    """Сканирование QR-кодов с веб-камеры"""
    global stop_event, pause_event
    
    if filter_warnings:
        warnings.filterwarnings("ignore", message=".*double decoding failed.*")
    
    print("[INFO] Запуск веб-камеры...")
    vs = None
    qr_reader = QReader()
    SearchQRcode = set()
    dic = {}
    frame_count = 0
    window_name = "QR Code Scanner - Камера"
    
    try:
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        
        while not stop_event.is_set():
            if pause_event.is_set():
                frame = vs.read()
                if frame is not None:
                    frame_resized = cv2.resize(frame, (640, 480))
                    cv2.putText(frame_resized, "PAUSE", (200, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
                    cv2.imshow(window_name, frame_resized)
                
                key = cv2.waitKey(100) & 0xFF
                if key == ord('q'):
                    break
                if _check_window_close(window_name):
                    print("[INFO] Окно закрыто через крестик. Остановка камеры...")
                    break
                continue
            
            frame_count += 1
            frame = vs.read()
            if frame is None:
                print("[ERROR] Не удалось получить кадр с камеры")
                break
            
            if PredProc == 1:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.GaussianBlur(frame, (7, 7), 0)
                frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)
                h, w = frame.shape[:2]
                frame = cv2.resize(frame, (w, h))
            
            qr_codes = False
            if frame_count % skip_frame == 0:
                qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)
                for key in list(dic.keys()):
                    if key not in valid_text:
                        del dic[key]
            else:
                for key, value in dic.items():
                    bbox_show(frame, (value[0], value[1]), (value[2], value[3]), key, value[4])
            
            if qr_codes:
                for i in range(len(qr_codes[0])):
                    name = qr_codes[0][i]
                    if name is None:
                        print('[WARNING] QR-code не прочитан')
                        continue
                    
                    print(f'[DETECTED] QR-code: {name}')
                    SearchQRcode.add(name)
                    
                    barcodeData = qr_codes[1][i]
                    try:
                        x1 = int(barcodeData['bbox_xyxy'][0])
                        y1 = int(barcodeData['bbox_xyxy'][1])
                        x2 = int(barcodeData['bbox_xyxy'][2])
                        y2 = int(barcodeData['bbox_xyxy'][3])
                        dic[name] = [x1, y1, x2, y2, name in valid_text]
                        bbox_show(frame, (x1, y1), (x2, y2), name, name in valid_text)
                    except Exception as e:
                        print(f"[ERROR] Ошибка bbox: {e}")
            
            frame_resized = cv2.resize(frame, (640, 480))
            cv2.imshow(window_name, frame_resized)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if _check_window_close(window_name):
                print("[INFO] Окно закрыто через крестик. Остановка камеры...")
                break
    
    except Exception as e:
        print(f"[ERROR] Ошибка в camera_scanning: {e}")
    
    finally:
        cv2.destroyAllWindows()
        if vs is not None:
            vs.stop()
        stop_event.clear()
        pause_event.clear()
        print("[INFO] Камера отключена. Возврат в приложение...")
    
    return SearchQRcode


def realtime_scanning(video_path: str, valid_text: list, skip_frame: int, PredProc: int, filter_warnings: bool=True) -> set:
    """Сканирование QR-кодов из видеофайла с отображением"""
    global stop_event, pause_event
    
    if filter_warnings:
        warnings.filterwarnings("ignore", message=".*double decoding failed.*")
    
    print(f"[INFO] Открытие видеофайла: {video_path}")
    cap = None
    qr_reader = QReader()
    SearchQRcode = set()
    dic = {}
    frame_count = 0
    window_name = "QR Code Scanner"
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"[ERROR] Не удалось открыть видео: {video_path}")
            return set()
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"[INFO] Видео открыто. Всего кадров: {total_frames}")
        
        while not stop_event.is_set():
            if pause_event.is_set():
                ret, frame = cap.read()
                if ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1)
                    if PredProc == 1:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame_resized = cv2.resize(frame, (640, 480))
                    cv2.putText(frame_resized, "PAUSE", (200, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
                    curr = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    cv2.putText(frame_resized, f"Frame: {curr}/{total_frames}", 
                               (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.imshow(window_name, frame_resized)
                
                key = cv2.waitKey(100) & 0xFF
                if key == ord('q'):
                    break
                if _check_window_close(window_name):
                    print("[INFO] Окно закрыто через крестик. Остановка видео...")
                    break
                continue
            
            frame_count += 1
            ret, frame = cap.read()
            if not ret:
                print("[INFO] Конец видео.")
                break
            
            if PredProc == 1:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.GaussianBlur(frame, (7, 7), 0)
                frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                frame = cv2.resize(frame, (w, h))

            qr_codes = False
            if frame_count % skip_frame == 0:
                qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)            
                for key in list(dic.keys()):
                    if not key in valid_text:
                        del dic[key]
            else:
                for key, value in dic.items():
                    bbox_show(frame, (value[0], value[1]), (value[2], value[3]), key, value[4])
            
            if qr_codes:
                for i in range(len(qr_codes[0])):
                    name = qr_codes[0][i]
                    if name is None:
                        print('[WARNING] QR-code не прочитан')
                        continue
                    
                    print(f'[DETECTED] QR-code: {name}') 
                    SearchQRcode.add(name)             

                    barcodeData = qr_codes[1][i]
                    try:
                        x1 = int(barcodeData['bbox_xyxy'][0])
                        y1 = int(barcodeData['bbox_xyxy'][1])
                        x2 = int(barcodeData['bbox_xyxy'][2])
                        y2 = int(barcodeData['bbox_xyxy'][3])
                        dic[name] = [x1, y1, x2, y2, name in valid_text]
                        bbox_show(frame, (x1, y1), (x2, y2), name, name in valid_text)
                    except Exception as e:
                        print(f"[ERROR] Ошибка bbox: {e}")

            print(f"[INFO] Кадр: {frame_count}")
            frame_resized = cv2.resize(frame, (640, 480))
            cv2.imshow(window_name, frame_resized)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("[INFO] Остановка клавишей 'q'")
                break
            if _check_window_close(window_name):
                print("[INFO] Окно закрыто через крестик. Остановка видео...")
                break
    
    except Exception as e:
        print(f"[ERROR] Ошибка в realtime_scanning: {e}")
    
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        stop_event.clear()
        pause_event.clear()
        print("[INFO] Видео закрыто. Возврат в приложение...")
    
    return SearchQRcode


def scanning(video_path: str, valid_text: list, output_path: str, skip_frame: int, 
             PredProc: int, filter_warnings: bool=True) -> set:
    """Сканирование с сохранением результата в файл"""
    if filter_warnings:
        warnings.filterwarnings("ignore", message=".*double decoding failed.*")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] Не удалось открыть видео: {video_path}")
        exit()
    
    qr_reader = QReader()
    file_path = asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not file_path:
        print("[INFO] Сохранение отменено")
        cap.release()
        return set()
    
    new_video = cv2.VideoWriter(file_path, fourcc=cv2.VideoWriter.fourcc(*'mp4v'), 
                                fps=30, frameSize=(1920, 1080))
    SearchQRcode = set()
    lastQR = {}
    frame_count = 0
    
    while True:
        frame_count += 1
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Конец видео.")
            break
        
        if PredProc == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        qr_codes = False
        if frame_count % skip_frame == 0:
            qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)
            for key in list(lastQR.keys()):
                if not key in valid_text:
                    del lastQR[key]
        else:
            for key, value in lastQR.items():
                bbox_show(frame, (value[0], value[1]), (value[2], value[3]), key, value[4])

        if qr_codes:
            for i in range(len(qr_codes[0])):
                name = qr_codes[0][i]
                if name is None:
                    print('[WARNING] QR-code не прочитан')
                    continue
                print(f'[DETECTED] QR-code: {name}')
                SearchQRcode.add(name)    
                barcodeData = qr_codes[1][i]
                try:
                    x1 = int(barcodeData['bbox_xyxy'][0])
                    y1 = int(barcodeData['bbox_xyxy'][1])
                    x2 = int(barcodeData['bbox_xyxy'][2])
                    y2 = int(barcodeData['bbox_xyxy'][3])
                    lastQR[name] = [x1, y1, x2, y2, name in valid_text]
                    bbox_show(frame, (x1, y1), (x2, y2), name, name in valid_text)
                except Exception as e:
                    print(f"[ERROR] Ошибка bbox: {e}")
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        print(frame_count)
        new_video.write(frame)
    
    cap.release()
    new_video.release()
    return SearchQRcode