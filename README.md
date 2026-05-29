# UniRank 🎓

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt-6-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**UniRank**, üniversiteleri çeşitli metrikler ve ağırlıklara göre sıralayan, analiz eden ve veritabanındaki bilgileri sezgisel bir arayüzle sunan modern bir masaüstü uygulamasıdır. Yükseköğretim araştırmalarını kolaylaştırmak için PyQt6 tabanlı, duyarlı ve özel tasarımlı bir gösterge paneli (dashboard) sunar.

## 🚀 Özellikler

- **Gelişmiş Arama ve Filtreleme:** Üniversite adı, etiketler (hashtags) ve özel anahtar kelimeler ile anında filtreleme.
- **Dinamik Puanlama:** Ağırlıklandırılmış metriklerle (Maliyet, Akademik Başarı, Konum vb.) anlık skor hesaplama.
- **Modern Arayüz (UI):** Premium karanlık/aydınlık tema seçenekleri, mikro animasyonlar ve şık bileşenler.
- **Detay Çekmecesi (Drawer):** İlgilendiğiniz üniversitenin tüm detaylarını tek bir panelde, kolay okunabilir bir formatta görüntüleme.
- **Tamamen Modüler Yapı:** Esnek ve genişletilebilir `core`, `ui`, `utils` mimarisi.

## 📁 Proje Mimarisi

Proje kodları temiz ve sürdürülebilir olması amacıyla modüler bir yapıda tasarlanmıştır:
```text
UniRank/
├── main.py                    # Uygulamanın ana giriş noktası (Entry point)
├── requirements.txt           # Bağımlılıklar (Dependencies)
├── data_base/                 # JSON tabanlı üniversite veri setleri
├── unirank/                   # Ana Uygulama Paketi
│   ├── core/                  # Veri yükleme ve modeller (json_loader.py, models.py)
│   ├── ui/                    # Arayüz bileşenleri (main_window.py, widgets.py, theme.py)
│   └── utils/                 # Araçlar, algoritmalar ve yardımcılar (helpers.py)
└── tests/                     # Birim testleri (Unit tests)
```

## 🛠️ Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/ayberkdt/UniRank.git
cd UniRank
```

### 2. Gerekli Kütüphaneleri Kurun
Projeyi sanal bir ortamda (virtualenv) kurmanız önerilir:
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
```bash
python main.py
```

## 📦 Dağıtım (Executable Yapma)

Eğer projeyi Python yüklü olmayan bir bilgisayarda (örneğin Windows) çalıştırılabilen bir `.exe` dosyası haline getirmek isterseniz `build.py` scriptini kullanabilirsiniz:

```bash
pip install pyinstaller
python build.py
```
İşlem tamamlandıktan sonra `dist/UniRank` klasörü içerisinde `UniRank.exe` dosyasını bulabilirsiniz.

## 🤝 Katkıda Bulunma

Hata bildirimleri ve yeni özellik istekleri için lütfen [Issues](../../issues) bölümünü kullanın veya Pull Request açın.
