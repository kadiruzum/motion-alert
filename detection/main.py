#gerekli kütüphanelerin yüklenmesi
import cv2
from video_processor import VideoProcessor
from rectangle_detector import RectangleDetector
from motion_detector import MotionDetector

def main(video_path):
    video_processor = VideoProcessor(video_path)
    rectangle_detector = RectangleDetector()
    motion_detector = MotionDetector()

    while True:
        frame = video_processor.get_frame()
        if frame is None:
            break
        
        # tespit edilecek alan (dikdortgenle belirttigim alan)
        roi_coordinates = rectangle_detector.detect_red_rectangle(frame)

        if roi_coordinates:
            # hareket tespiti yaptigimiz fonksiyon
            motion_detector.detect_motion(frame, roi_coordinates)

        # ekrana goruntuyu yazdirma
        cv2.imshow('Frame', frame)

        # q tusu ile videodan cikis
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_processor.release()

# video yolu
video_path = '../media/videos/inputUpdate1.mp4'  

main(video_path)
