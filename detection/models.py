from django.db import models

# Ortak özellikleri barındıran BaseEvent sınıfı
class BaseEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Bu alan, kayıt oluşturulduğu zamanı otomatik olarak kaydeder
    updated_at = models.DateTimeField(auto_now=True)  # Bu alan, kayıt her güncellendiğinde zaman bilgisini otomatik alır
    is_active = models.BooleanField(default=True)  # Kayıt aktif mi, değil mi? Başlangıçta aktif olarak kabul ederiz

    class Meta:
        abstract = True  # Bu sınıf doğrudan veritabanında tablo oluşturmaz, yalnızca başka sınıflara miras bırakılabilir

# BaseEvent'ten türeyen MotionEvent sınıfı
class MotionEvent(BaseEvent):
    motion_start_time = models.DateTimeField(null=False)  # Hareketin başladığı zamanı kaydediyoruz, zorunlu alan
    motion_end_time = models.DateTimeField(null=True, blank=True)  # Hareketin bitiş zamanı, bu alan boş bırakılabilir çünkü başlangıç zamanı da yeterli olabilir

    def __str__(self):
        return f"Motion Event: {self.motion_start_time} - {self.motion_end_time}"  # Bu, objenin str() metodu ile daha anlamlı bir gösterim sağlıyor
