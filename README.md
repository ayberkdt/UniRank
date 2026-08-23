# UniRank 🎓

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**UniRank**, üniversiteleri çeşitli metrikler ve ağırlıklara göre sıralayan, analiz eden ve veritabanındaki bilgileri sezgisel bir arayüzle sunan bir web uygulamasıdır. FastAPI tabanlı bir backend ve dinamik bir web arayüzü sunar; Vercel üzerinden bulutta çalışır.

## 🚀 Özellikler

- **Gelişmiş Arama ve Filtreleme:** Üniversite adı, etiketler (hashtags) ve özel anahtar kelimeler ile anında filtreleme.
- **Dinamik Puanlama:** Ağırlıklandırılmış metriklerle (Maliyet, Akademik Başarı, Konum vb.) anlık skor hesaplama.
- **Modern Web Arayüzü (UI):** Vanilla HTML, CSS ve JavaScript ile geliştirilmiş, mikro animasyonlar ve şık bileşenler barındıran duyarlı (responsive) tasarım.
- **Hızlı Backend:** FastAPI altyapısı ile `data_base` klasöründeki JSON verilerinin hızlı ve güvenli sunumu.
- **Vercel Entegrasyonu:** Serverless mimari ile kolay dağıtım (`vercel.json`).

## 📁 Proje Mimarisi

```text
UniRank/
├── api/                       # Vercel için FastAPI uç noktaları (index.py)
├── public/                    # Web frontend dosyaları (index.html, script.js, style.css)
├── data_base/                 # JSON tabanlı üniversite veri setleri
├── unirank/                   # Veri katmanı paketi
│   ├── core/                  # Veri yükleme, şema ve bütünlük kontrolleri (json_loader.py vb.)
│   └── utils/                 # Araçlar, algoritmalar ve yardımcılar
├── scripts/                   # Veri güncelleme ve doğrulama scriptleri (devServer.mjs dahil)
├── vercel.json                # Vercel dağıtım yapılandırması
└── requirements.txt           # Python bağımlılıkları
```

## 🛠️ Kurulum ve Çalıştırma

Uygulama Vercel üzerinde çalışır; aşağıdaki adımlar yalnızca dağıtım öncesi yerel önizleme içindir.

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/ayberkdt/UniRank.git
cd UniRank
```

### 2. Gerekli Kütüphaneleri Kurun
```bash
pip install -r requirements.txt
```

### 3. Yerel Önizleme (isteğe bağlı)

Statik arayüz + veri API'sini birlikte sunan hafif geliştirme sunucusu:
```bash
node scripts/devServer.mjs
```
Tarayıcıda `http://localhost:8765` adresini açın. Alternatif olarak yalnızca API için: `uvicorn api.index:app --reload`.

Dağıtım öncesi temel frontend sözleşmeleri:
```bash
node scripts/checkStaticAssets.mjs
node scripts/checkWebUi.mjs
node scripts/checkDeadlineDashboard.mjs
node scripts/checkScholarships.mjs
node scripts/checkResearchPathways.mjs
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

## Research Integrity

All university research and database updates must follow `AGENTS.md` and the skills under `skills/`.

Before adding or updating a university record, run:

1. `skills/university-research/SKILL.md`
2. `skills/source-verification/SKILL.md`
3. `skills/student-sentiment/SKILL.md`
4. `skills/data-normalization/SKILL.md`
5. `skills/quality-control/SKILL.md`

Do not add unsourced values to the database.
