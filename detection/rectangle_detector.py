import cv2
import numpy as np

class RectangleDetector:
    def __init__(self):
        pass  # Şu an için özel bir şey yapmamıza gerek yok, ama ileride eklenebilir diye koyduk

    def detect_red_rectangle(self, frame):
        # BGR'den HSV'ye dönüşüm yapıyoruz çünkü kırmızı rengi daha kolay seçmek için HSV kullanmak mantıklı
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Kırmızı rengin alt ve üst sınırlarını belirliyoruz, yoksa maske yanlış olur
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])

        # İlk kırmızı tonlarını yakalayan maske oluşturuyoruz
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Kırmızının diğer tonlarını da kaçırmamak için ikinci bir aralık belirliyoruz
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        # İki maskeyi birleştiriyoruz ki tüm kırmızı tonlarını kapsayalım
        mask = mask | mask2

        # Maske ile orijinal görüntüyü birleştirerek sadece kırmızı alanları bırakıyoruz
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Şekilleri daha net anlamak için gri tonlamaya geçiyoruz
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)  # İkili bir görüntü elde ediyoruz

        # Konturları buluyoruz, çünkü dikdörtgen olup olmadığını konturlar belirleyecek
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Küçük gürültüleri dikkate almıyoruz, 1000 px'den küçük olanlar iptal
                # Konturu sadeleştiriyoruz, daha az nokta olsun diye
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) == 4:  # Eğer 4 köşesi varsa, bu bir dikdörtgendir
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)  # Dikdörtgeni yeşil çerçeveyle çiziyoruz
                    roi_coordinates = cv2.boundingRect(approx)  # Dikdörtgenin ROI'sini alıyoruz
                    return roi_coordinates
        return None  # Eğer dikdörtgen bulamazsak, None döneriz
