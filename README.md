Projenin Amacı

Bu proje, izinsiz hareketlerin tespit edilmesi ve bu hareketlerin kaydedilmesi amacıyla geliştirilmiştir. Hareket algılandığında, başlangıç ve bitiş zamanları veritabanına kaydedilir. Ayrıca, belirli bir bölgeye izinsiz giriş olduğunda alarm çalar ve kullanıcıya canlı bir video akışı üzerinde alarm uyarısı gösterilir.

Kullanılan Teknolojiler

Django Framework: Backend geliştirme için kullanıldı.

OpenCV: Hareket algılama ve video işleme.

Pygame: Alarm sesi oynatma.

HTML, CSS, JavaScript: Kullanıcı arayüzü tasarımı.

SQLite: Veritabanı yönetimi.

Kurulum ve Çalıştırma

Gereksinimler

Python 3.8 veya üzeri

Pip (Python Package Manager)





Kurulum Adımları




Proje Deposu:

Proje dosyalarını indirin veya kopyalayın.
git clone <proje-depo-url>
cd <proje-dizini>

Gerekli Paketlerin Yüklenmesi:

Gerekli kütüphaneleri yükleyin.
pip install -r requirements.txt

Veritabanı Migrasyonu:

Veritabanını hazırlayın.
python manage.py migrate

Statik Dosyaları Toplama:

Statik dosyaları toplayın.
python manage.py collectstatic

Sunucuyu Çalıştırma:

Projeyi başlatın.
python manage.py runserver
