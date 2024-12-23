import cv2
import datetime
import pygame
from .models import MotionEvent  # Django modelini içeri aktar
from django.utils import timezone


class MotionDetector:
    def __init__(self):
        # Arka plan çıkarma işlemini başlatıyoruz. Bu, hareketleri tespit etmemizi sağlar.
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=4000, varThreshold=20, detectShadows=False)
        self.frame_count = 0  # Isınma süresi için kare sayacını başlatıyoruz
        self.motion_active = False  # Hareketin aktif olup olmadığını takip edeceğiz
        self.motion_start_time = None  # Hareketin ne zaman başladığını bileceğiz
        self.motion_end_time = None  # Hareketin bitiş zamanını kaydedeceğiz

        # Pygame ses modülünü başlatıyoruz. Alarm sesini çalabilmek için
        pygame.mixer.init()
        self.alarm_sound = pygame.mixer.Sound("media/alarm_sounds/alarm.wav")  # Alarm ses dosyasının yolu

    def detect_motion(self, frame, roi_coordinates):

        self.motion_start_time = timezone.localtime(timezone.now())  # Hareketin başladığı anı alıyoruz (aware datetime)
        self.motion_end_time = timezone.localtime(timezone.now())  # Bitiş zamanını da aware datetime olarak tutuyoruz

        # Şu anki zamanı alıyoruz, canlı saat göstereceğiz çünkü :)
        now = datetime.datetime.now()
        time_text = now.strftime("%Y-%m-%d %H:%M:%S")  # Tarih ve saat formatı

        # Her kareye canlı saati ekliyoruz ki zamanı görebilelim
        cv2.putText(
            frame,
            time_text,
            (10, 30),  # Saati yerleştireceğimiz konum
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),  # Beyaz renk, saatin görünürlüğü için
            2,
            cv2.LINE_AA
        )

        # Isınma süresi: İlk 50 kareyi sadece arka plan modelini eğitmek için kullanıyoruz, sonrasında hareket tespiti yapacağız
        self.frame_count += 1
        if self.frame_count < 50:
            self.fgbg.apply(frame)
            return

        fgmask = self.fgbg.apply(frame)  # Arka plan çıkarma işlemi
        fgmask[fgmask == 127] = 0  # Gölgeleri görmemek için maskeleme yapıyoruz
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > 700:  # Yalnızca büyük hareketleri dikkate alıyoruz (yakın mesafedeki küçük hareketleri geçiyoruz)
                (cx, cy, cw, ch) = cv2.boundingRect(contour)

                # ROI'ye (Region of Interest) girip girmediğini kontrol ediyoruz, çünkü sadece bu bölgeyi izlemek istiyoruz
                x, y, w, h = roi_coordinates
                if (cx + cw > x and cx < x + w) and (cy + ch > y and cy < y + h):
                    motion_detected = True
                    # Alarm mesajını ekliyoruz, yani izinsiz bölgeye hareket olursa alarm çalsın
                    cv2.putText(
                        frame,
                        "ALARM! Izinsiz Bolge Hareketi!",
                        (10, 70),  # Alarm mesajının eklenmesi için yer
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),  # Kırmızı renk, dikkat çekici olsun
                        2,
                        cv2.LINE_AA
                    )

                    # Hareket başladığında, sadece bir kez yazdırmak için
                    if not self.motion_active:
                        self.motion_active = True
                        self.motion_start_time = now
                        print(f"Hareket tespit edildi - Başlangıç: {self.motion_start_time.strftime('%H:%M:%S')}")

                        motion_event = MotionEvent.objects.create(
                            motion_start_time=self.motion_start_time,
                            motion_end_time=None  # Bitiş zamanı henüz yok
                        )
                    
                        self.alarm_sound.play(loops=-1)  # Alarm sesini başlatıyoruz, durdurulana kadar çalsın

                # Hareket eden cisimlerin etrafına dikdörtgen çiziyoruz ki görsel olarak tespit edelim
                cv2.rectangle(frame, (cx, cy), (cx + cw, cy + ch), (0, 0, 0), 2)  # Siyah dikdörtgen, hareketi vurguluyor

        # Hareket sona erdiğinde, alarmı durdurup mesajı güncelliyoruz
        if not motion_detected and self.motion_active:
            self.motion_active = False
            self.motion_end_time = now
            print(f"Hareket sona erdi - Bitiş: {self.motion_end_time.strftime('%H:%M:%S')}")

             # Son hareket kaydını bulup bitiş zamanını güncelliyoruz
            last_motion_event = MotionEvent.objects.filter(motion_end_time__isnull=True).last()
            if last_motion_event:
                last_motion_event.motion_end_time = self.motion_end_time
                last_motion_event.save()  # Hareketin bitiş zamanını kaydediyoruz
            
            # Alarm durduğunda sesi durduruyoruz
            pygame.mixer.stop()  # Alarm sesini durduruyoruz
