# UniRank Araştırma ve Ürün Geliştirme Süreci

Bu belge, üniversite verisinin araştırılmasından kullanıcı arayüzünde yayınlanmasına kadar izlenen çalışma akışını kaydeder. Amaç yalnızca daha fazla kayıt eklemek değil; öğrencinin başvuru, maliyet, burs, araştırma uyumu ve risk kararını güvenilir kanıtlarla verebilmesini sağlamaktır.

## 1. İsteği karar alanlarına ayırma

Her çalışma önce somut karar alanlarına bölünür: program uygunluğu, kabul koşulları, gerekli belgeler, öğretim dili, başvuru tarihi, ücretler, burslar, yaşam maliyeti, barınma, araştırma grupları, laboratuvarlar ve akademik iletişim bilgileri.

Araştırma ve arayüz işleri ayrı teslimatlar olarak izlenir. Böylece görsel bir iyileştirme, doğrulanmamış bir veriyi doğruymuş gibi öne çıkarmaz.

## 2. Ajan görevlerinin tanımlanması

Kullanıcı paralel ajan çalışması istediğinde görevler ülke veya kanıt alanı bazında, birbirinin üzerine yazmayacak şekilde ayrılır. Örnek görevler:

- Avrupa kabul tarihleri ve gerekli belgeler
- ABD kabul tarihleri, ücretler ve finansman
- Burs uygunluğu, son tarihler ve başvuru adımları
- En güçlü programların öğretim üyeleri, resmî e-posta adresleri, laboratuvarları ve araştırma altyapısı

Her ajan aynı veri bütünlüğü kurallarına uyar. Sonuç, doğrudan ana veritabanına yazılmak yerine `research_queue/enrichment/` altında kaynaklı bir zenginleştirme yükü olarak hazırlanır.

## 3. Resmî kaynak araştırması

Kritik alanlarda öncelik sırası program, kabul, müfredat, ücret, burs, bölüm/laboratuvar ve resmî kamu sayfalarıdır. Bir URL erişilebilirlik, güncellik ve ilgili alanı gerçekten destekleyip desteklemediği açısından kontrol edilir.

Öğretim üyesi e-postası yalnızca adresi açıkça yayımlayan resmî sayfayla birlikte kaydedilir. Burs başvuru adımı yalnızca resmî burs veya mali yardım sayfasına dayanır. Kaynak bulunamazsa değer tahmin edilmez; `unknown`, `null`, boş liste veya `needs_verification` kullanılır.

## 4. Zenginleştirme yükü ve kaynak kapsamı

Yeni bulgular program bazında hazırlanır; farklı programlar tek kayıtta birleştirilmez. Her kritik değişiklik için:

- kaynak URL'si ve başlığı,
- kaynak türü ve erişim durumu,
- son kontrol tarihi,
- desteklediği alanlar,
- güven seviyesi ve açıklama

kaydedilir. Kullanıcıya görünen açıklamalar İngilizce ve Türkçe olarak tutulur.

## 5. Kontrollü birleştirme

Zenginleştirmeler `scripts/apply_enrichment.py` ile uygulanır. Betik, karar profilini değiştirip o alanı kapsayan kaynak sunmayan yükleri reddeder. Birleştirmeden sonra kategoriler `scripts/standardize_categories.py --write` ile ortak sözlüğe göre standartlaştırılır.

## 6. Kalite kontrolü

Her veri turunda şu sıra izlenir:

1. Kaynak kapsamı ve bozuk bağlantı kontrolü
2. Alan bazlı güven seviyelerinin gözden geçirilmesi
3. `checklists/canary_tests.md` kontrolleri
4. Otomatik test paketi
5. Değişiklik farklarının ve veri sözleşmelerinin denetlenmesi

Canary veya test başarısızsa kayıt tamamlandı sayılmaz. Eksik veri kabul edilebilir; kaynaksız kesinlik kabul edilmez.

## 7. Arayüz geliştirme akışı

Arayüz çalışması şu soruyla başlar: öğrenci ilk bakışta hangi kararı verebilmeli? Üniversite kartlarında bilgi sırası bu nedenle kimlik, teknik uyum ve veri güveni, eğitim biçimi, maliyet, son tarih, barınma riski ve eylemler şeklindedir.

Yeni kart tasarımında:

- ülke bayrağı sağ kenarda, veriyi örtmeyen kontrollü bir filigran olarak korunur,
- masaüstünde her program tek satıra yayılan yatay bir kartta gösterilir,
- küçük ve okunması zor etiketler büyütülür,
- dört temel karar alanı aynı düzende gösterilir,
- ikincil maliyet ve risk bilgileri ayrı bir satıra alınır,
- favori, karşılaştırma ve ayrıntı eylemleri birbirinden açıkça ayrılır.

## 8. Yan yana karşılaştırma davranışı

Bir kullanıcı en fazla üç programı karşılaştırma listesine ekleyebilir. Seçim tarayıcıda saklandığı için sayfa yenilendiğinde korunur. Karşılaştırma çalışma alanı en az iki seçimle açılır ve şu alanları hizalı sütunlarda gösterir:

- program ve eğitim biçimi,
- yıllık maliyet, başvuru ücreti, aylık yaşam maliyeti ve güncel son tarih,
- kabul ve barınma riskleri,
- burs/finansman rotası,
- araştırma uyumu,
- veri kalitesi ve kontrol edilmiş resmî kaynak sayısı.

Masaüstünde sütunlar aynı anda görünür. Dar ekranlarda sütun düzeni korunur ve yatay kaydırmayla incelenir; kartlar okunamayacak kadar daraltılmaz.

## 9. Bilgi detayında karar akışı

Detay çekmecesi üniversite ve program kimliğini sabit başlıkta korur. İçerik sırası, uzun bir veri dökümü yerine öğrencinin karar verme sırasını izler:

1. Üniversite, program, konum ve veri güveni
2. Genel sonuç ve dört kritik karar alanı
3. Aktif ağırlıklardan otomatik hesaplanan karar profili
4. Dil/sınav/belge özeti, kalan süre ve resmî bağlantılar
5. Başvuru gereklilikleri
6. İsteğe bağlı akademik, maliyet/yaşam ve kanıt ayrıntıları

Karar profilindeki altı eksen `scoring.js` çıktısından 0–100 ölçeğinde okunur; elle kopyalanmış ayrı bir grafik verisi tutulmaz. Kırmızı riskli, sarı dengeli ve yeşil güçlü sonucu gösterir. Grafik tek başına renge bağlı değildir: her eksenin adı, sayısal değeri ve durum metni yanında listelenir.

Uzun bölümler varsayılan olarak katlı tutulur. Başvuru gereklilikleri ilk açılışta görünür; müfredat, laboratuvar, hoca, maliyet dayanağı, burs, konaklama ve kaynak günlüğü kullanıcı istediğinde açılır. Bu düzen veri kapsamını azaltmaz, ilk okumadaki bilişsel yükü azaltır.

## 10. Yayın öncesi ürün kontrolü

JavaScript sözdizimi, çeviri anahtarları, erişilebilir adlar, klavye ile kapatma, kalıcı seçim ve duyarlı yerleşim kontrol edilir. Uygulamanın yerel API ile açıldığı doğrulanır. Veri araştırması içeren bir sürümde bunlara canary ve tam test paketi de eklenir.

Bu süreç yaşayan bir kayıttır. Yeni bir veri alanı veya kullanıcı akışı eklendiğinde, araştırma kaynağı ve yayın öncesi kontrolüyle birlikte bu belgeye de işlenmelidir.
