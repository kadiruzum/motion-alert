import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import subprocess
from django.http import HttpResponse
import datetime
from .models import MotionEvent
from django.utils.dateparse import parse_datetime

def select_video(request):
    return render(request, 'detection/select_video.html')  # Video seçme ekranını gösteriyoruz çünkü kullanıcının seçim yapması gerekiyor

@csrf_exempt  # Bu CSRF kontrolünü devre dışı bırakıyor, yoksa hata alırdık (tabii bu geliştirme ortamı için)
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']

        # Medya dosyasını koyacağımız klasörün yolunu belirliyoruz
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
        os.makedirs(upload_dir, exist_ok=True)  # Klasör yoksa oluşturuyoruz çünkü yoksa hata verir

        file_path = os.path.join(upload_dir, video_file.name)

        try:
            # Dosyayı parça parça okuyup diske yazıyoruz, yoksa büyük dosyalar sıkıntı çıkarır
            with open(file_path, 'wb') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            # Her şey yolundaysa başarı mesajını dönüyoruz
            return JsonResponse({'message': f"{video_file.name} başarıyla kaydedildi."})

        except Exception as e:
            # Burada bir şeyler ters giderse hata mesajı dönüyoruz
            return JsonResponse({'error': f"Yükleme sırasında bir hata oluştu: {str(e)}"}, status=400)
    
    return JsonResponse({'error': 'Video dosyası bulunamadı.'}, status=400)

import cv2
from django.http import StreamingHttpResponse
from .video_processor import VideoProcessor
from .rectangle_detector import RectangleDetector
from .motion_detector import MotionDetector

def generate_frames(video_name):
    # Burada video dosyasının tam yolunu dinamik olarak oluşturuyoruz
    video_path = os.path.join('media', 'videos', video_name)
    
    if not os.path.exists(video_path):
        # Video dosyası yoksa buradan patlar, o yüzden hata fırlatıyoruz
        raise FileNotFoundError(f"Video bulunamadı: {video_path}")
    
    # Video işleme sınıflarını burada başlatıyoruz, her bir işlemci işini ayrı yapacak
    video_processor = VideoProcessor(video_path)
    rectangle_detector = RectangleDetector()
    motion_detector = MotionDetector()

    while True:
        frame = video_processor.get_frame()
        if frame is None:
            break  # Eğer kareler bitmişse döngüden çıkıyoruz, daha fazla iş yok

        # Kırmızı dikdörtgen arıyoruz, çünkü bizim alanımız bu
        roi_coordinates = rectangle_detector.detect_red_rectangle(frame)

        if roi_coordinates:
            # Eğer ROI bulduysak hareket algılamayı burada yapıyoruz
            motion_detector.detect_motion(frame, roi_coordinates)

        # Frame'i burada JPEG formatına çeviriyoruz, çünkü bu format daha hızlı akıyor
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Burada her bir frame'i akış olarak gönderiyoruz, tarayıcı bunu görebiliyor
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    video_processor.release()  # Video işlemcisini bırakıyoruz yoksa kaynakları gereksiz yere tüketir


# API endpoint'i
from django.http import StreamingHttpResponse

def watch_video(request, video_name):
    try:
        # Video izleme için akış başlatıyoruz
        return StreamingHttpResponse(
            generate_frames(video_name),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
    except FileNotFoundError:
        # Eğer video yoksa hata mesajı dönüyoruz
        return JsonResponse({'error': 'Seçilen video bulunamadı.'}, status=404)


def list_videos(request):
    # Videoların bulunduğu klasörü tarıyoruz
    video_folder = os.path.join(settings.MEDIA_ROOT, 'videos')
    video_files = [
        {'name': video, 'url': f"{settings.MEDIA_URL}videos/{video}"}
        for video in os.listdir(video_folder)
        if video.endswith(('.mp4', '.avi', '.mov', '.mkv'))  # Sadece belirli formatları alıyoruz yoksa saçma şeyler çıkar
    ]
    return render(request, 'detection/videos.html', {'videos': video_files})

def create_motion(request):
    if request.method == "POST":
        # Burada gelen POST verilerini çekiyoruz
        motion_start_time = request.POST.get('motion_start_time')
        motion_end_time = request.POST.get('motion_end_time')

        # Gelen zamanları kontrol ediyoruz çünkü format hatası olursa patlar
        try:
            motion_start_time = parse_datetime(motion_start_time)
            motion_end_time = parse_datetime(motion_end_time)

            if motion_start_time and motion_end_time:
                # Eğer her şey doğruysa veritabanına yazıyoruz
                MotionEvent.objects.create(
                    motion_start_time=motion_start_time,
                    motion_end_time=motion_end_time
                )
                return redirect('motion_list')  # İşlem başarılıysa listeye dön
            else:
                error = "Geçersiz tarih formatı. Lütfen tekrar deneyin."  # Kullanıcıya dönmesi için hata mesajı yazıyoruz
        except Exception as e:
            # Ne olur ne olmaz diye burada da genel bir hata kontrolü var
            error = f"Hata: {str(e)}"
        
        # Eğer hata varsa, formu yeniden hata mesajıyla gösteriyoruz
        return render(request, 'detection/create_motion.html', {'error': error})

    # Eğer GET isteği gelmişse formu normal şekilde gösteriyoruz
    return render(request, 'detection/create_motion.html')

def motion_list(request):
    motions = MotionEvent.objects.all()  # Veritabanından tüm hareket kayıtlarını alıyoruz
    return render(request, 'detection/motions.html', {'motions': motions})

def motion_update(request, motion_id):
    motion = get_object_or_404(MotionEvent, id=motion_id)  # Harekete erişiyoruz, yoksa 404 döner
    if request.method == 'POST':
        # Kullanıcıdan gelen yeni bilgileri burada alıp güncelliyoruz
        motion.motion_start_time = request.POST.get('motion_start_time')
        motion.motion_end_time = request.POST.get('motion_end_time')
        motion.save()
        return redirect('motion_list')  # Güncelleme sonrası listeye yönlendiriyoruz
    return render(request, 'detection/motion_update.html', {'motion': motion})

def motion_delete(request, motion_id):
    motion = get_object_or_404(MotionEvent, id=motion_id)  # Silmek istediğimiz kaydı getiriyoruz
    motion.delete()  # Veritabanından siliyoruz, çünkü artık ihtiyacımız yok
    return redirect('motion_list')  # Silme işleminden sonra listeye yönlendiriyoruz
