import cv2

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)  # Burada video dosyasını açıyoruz, yoksa çerçeve okuyamayız

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None  # Video bitmişse ya da hata varsa None döneriz, yoksa sonsuz döngüde takılır
        return frame  # Her seferinde bir çerçeve dönüyoruz

    def release(self):
        self.cap.release()  # Kaynakları serbest bırakıyoruz, yoksa RAM dolabilir
        cv2.destroyAllWindows()  # Eğer açık bir pencere varsa (debug amaçlı), kapatıyoruz
