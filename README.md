# UniRank 🎓

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**UniRank**, üniversiteleri çeşitli metrikler ve ağırlıklara göre sıralayan, analiz eden ve veritabanındaki bilgileri sezgisel bir arayüzle sunan modern bir web ve masaüstü uygulamasıdır. Yükseköğretim araştırmalarını kolaylaştırmak için tasarlanmış, FastAPI tabanlı bir backend ve dinamik bir web arayüzü sunar. Proje aynı zamanda Vercel üzerinden bulutta çalışacak şekilde yapılandırılmıştır.

## 🚀 Özellikler

- **Gelişmiş Arama ve Filtreleme:** Üniversite adı, etiketler (hashtags) ve özel anahtar kelimeler ile anında filtreleme.
- **Dinamik Puanlama:** Ağırlıklandırılmış metriklerle (Maliyet, Akademik Başarı, Konum vb.) anlık skor hesaplama.
- **Modern Web Arayüzü (UI):** Vanilla HTML, CSS ve JavaScript ile geliştirilmiş, mikro animasyonlar ve şık bileşenler barındıran duyarlı (responsive) tasarım.
- **Hızlı Backend:** FastAPI altyapısı ile `data_base` klasöründeki JSON verilerinin hızlı ve güvenli sunumu.
- **Vercel Entegrasyonu:** Web sürümünün serverless mimari ile kolayca dağıtımı (`vercel.json`).
- **Masaüstü Desteği:** İsteğe bağlı olarak PyQt6 tabanlı yerel arayüz ile masaüstünde çalışma yeteneği (`main.py`).

## 📁 Proje Mimarisi

Proje kodları hem web hem de yerel kullanım senaryolarını destekleyecek şekilde tasarlanmıştır:
```text
UniRank/
├── api/                       # Vercel için FastAPI uç noktaları (index.py)
├── public/                    # Web frontend dosyaları (index.html, script.js, style.css)
├── data_base/                 # JSON tabanlı üniversite veri setleri
├── unirank/                   # Ana Uygulama Paketi
│   ├── core/                  # Veri yükleme ve modeller (json_loader.py vb.)
│   ├── ui/                    # Yerel masaüstü arayüz bileşenleri (PyQt6)
│   └── utils/                 # Araçlar, algoritmalar ve yardımcılar
├── vercel.json                # Vercel dağıtım yapılandırması
├── requirements.txt           # Python bağımlılıkları
└── main.py                    # Masaüstü sürümünün giriş noktası (PyQt6)
```

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel ortamınızda web sunucusu olarak veya masaüstü uygulaması olarak çalıştırabilirsiniz.

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/ayberkdt/UniRank.git
cd UniRank
```

### 2. Gerekli Kütüphaneleri Kurun
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın

**Web Sunucusu (FastAPI) Olarak:**
Uygulamayı yerel bir API sunucusu olarak başlatmak için uvicorn kullanabilirsiniz:
```bash
uvicorn api.index:app --reload
```
Daha sonra tarayıcınızda `public/index.html` dosyasını açarak (veya bir live server ile) web arayüzünü test edebilirsiniz.

**Masaüstü (PyQt6) Olarak:**
```bash
python main.py
```

## ☁️ Dağıtım (Vercel)

Proje, Vercel üzerinde barındırılmaya hazırdır. `vercel.json` dosyası, `api/` klasöründeki Python dosyalarını Serverless Fonksiyon, `public/` klasöründeki dosyaları ise statik içerik olarak sunacak şekilde yapılandırılmıştır.

Vercel CLI ile dağıtmak için:
```bash
npm i -g vercel
vercel
```

## 🤝 Katkıda Bulunma

Hata bildirimleri ve yeni özellik istekleri için lütfen [Issues](../../issues) bölümünü kullanın veya Pull Request açın.
