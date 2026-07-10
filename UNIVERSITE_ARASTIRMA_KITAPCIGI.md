# ÜNİVERSİTE ARAŞTIRMA VE VERİ GİRİŞİ KATI KURALLAR KİTAPÇIĞI (AGENT RULEBOOK)

Bu kitapçık, UniRank veri tabanı için üniversite ve yüksek lisans programı (özellikle Havacılık, Uzay, GNC, CFD, İtki, Yapısal Sistemler vb.) araştırması yapan tüm yapay zeka ajanlarının (agent) **KESİNLİKLE** uyması gereken kuralları ve standartları belirler. 

**AMACIMIZ:** Sıradan bir sıralama listesi yapmak değil; öğrencilerin "Gerçekten buraya başvurabilir miyim?", "Burs olanakları neler?", "Eğitim dili gerçekten İngilizce mi?", "Teknik olarak benim alanıma uygun mu?" gibi kritik sorularına **DOĞRULANMIŞ, RESMİ ve KESİN** yanıtlar sunmaktır.

Bu kuralların herhangi birinin ihlali, veri tabanının güvenilirliğini yok edeceği için KABUL EDİLEMEZ.

---

## 1. TEMEL YASAKLAR VE MUTLAK KURALLAR (ABSOLUTE RULES)

1. **ASLA TAHMİN ETME:** Hiçbir koşulda veri uydurulamaz (halüsinasyon yasaktır). Eğitim ücreti, son başvuru tarihi, burs olanakları, kabul şartları veya program durumu hakkında tahminde bulunamazsın.
2. **VERİ YOKSA "UNKNOWN" KULLAN:** Eğer bir değer resmi kaynaklardan doğrulanamıyorsa, alanı `unknown`, `null`, `[]` veya `needs_verification` olarak işaretle. Kendin bir değer atama.
3. **RESMİ KAYNAK ZORUNLULUĞU:** Her kritik veri alanı en az BİR adet resmi kaynağa (URL) dayanmalıdır. Resmi kaynaklar her zaman üçüncü parti kaynaklardan üstündür.
4. **FORUM BİLGİSİYLE GERÇEĞİ EZME:** Reddit, Quora, The Student Room, Discord vb. platformlardan alınan öğrenci yorumları ASLA resmi kabul, ücret, veya müfredat bilgisinin yerine geçemez. Bu kaynaklar SADECE öğrenci hissiyatı (sentiment) analizi için kullanılabilir.
5. **KIRIK (BROKEN) LİNKLER KAYNAK OLAMAZ:** Veri tabanına eklenen her URL mutlaka kontrol edilmelidir (Accessibility Check). Eğer sayfa ölü, arşivlenmiş veya erişilemez durumdaysa, bunu kanıt olarak kullanamazsın. Veri güvenilirliği `low` veya `unknown` olarak işaretlenmelidir.
6. **GENELLEME YAPMA:**
   - Üniversitenin genel prestiji, programın spesifik teknik kalitesi anlamına gelmez.
   - QS Genel Sıralaması yüksek diye, havacılık/uzay programı da iyidir varsayımı YAPILAMAZ.
   - Şehirde büyük bir havacılık şirketinin (örn. Airbus) bulunması, üniversite ile resmi partner oldukları anlamına GELMEZ. Partnerlik kanıtlanmalıdır.
   - Programın İngilizce web sayfası olması, derslerin %100 İngilizce işlendiği anlamına GELMEZ. Eğitim dili kesin olarak doğrulanmalıdır.
7. **ÇOKLU PROGRAMLARI BİRLEŞTİRME:** Her üniversite ve spesifik program çifti ayrı bir veri kaydıdır. "MSc Aerospace" ve "MSc Space Engineering" aynı üniversitede olsa bile ayrı ayrı incelenmelidir.

---

## 2. KAYNAK KULLANIM HİYERARŞİSİ

Bilgi ararken veya doğrularken kaynakları SADECE aşağıdaki öncelik sırasına göre dikkate al:

1. Üniversitenin resmi program sayfası.
2. Üniversitenin resmi kabul (admission) ve başvuru koşulları sayfası.
3. Resmi müfredat (curriculum) / ders kataloğu / çalışma planı.
4. Resmi eğitim ücreti ve harçlar sayfası.
5. Resmi burs / finansal destek / ulusal burs (örn. İtalya DSU) sayfaları.
6. Resmi departman / araştırma grubu / laboratuvar sayfaları.
7. Resmi devlet, bakanlık, vize ve göçmenlik portalları (Örn: Universitaly).
8. Üniversitenin resmi konaklama ve öğrenci işleri sayfası.
9. Resmi endüstri partnerinin / enstitünün işbirliğini doğrulayan sayfaları.
10. Güvenilir üçüncü parti veri tabanları (SADECE ikincil doğrulama için).
11. Öğrenci forumları, Facebook grupları, vb. (SADECE sentiment ve öğrenci görüşü için).

---

## 3. KRİTİK VERİ ALANLARI VE DOĞRULAMA PROTOKOLLERİ

Aşağıdaki alanların DİREKT OLARAK RESMİ KAYNAKTAN alınması ve kanıtlanması zorunludur.

### A. Program ve Müfredat Profili (Curriculum Profile)
- **Program Adı, Derece, Süre, ECTS:** Resmi program sayfasından doğrulanmalıdır.
- **Eğitim Dili (Teaching Language):** Gerekli minimum dil sertifikası (TOEFL/IELTS vs.) açıkça bulunmalıdır.
- **Dersler ve Uzmanlıklar (Tracks/Specializations):** "Aerospace" adı altında aslında "Mechanical" ağırlıklı bir müfredat işleniyorsa, bu durum not edilmeli ve sadece zorunlu dersler üzerinden teknik derinlik ölçülmelidir.

### B. Kabul Şartları (Eligibility Profile)
- **Geçmiş Derece (Previous Degree):** Hangi lisans bölümlerinden mezun olanların başvurabileceği doğrulanmalıdır.
- **Not Ortalaması ve Sınavlar:** Minimum GPA (veya eşdeğeri), GRE/GMAT, ve kredi bazlı ön koşullar (örn. "Matematikten minimum 30 ECTS") kesin olarak bulunmalıdır.
- **AB Dışı (Non-EU) Uygunluğu:** Programın AB dışı vatandaşlara (Non-EU/International) açık olup olmadığı kesinleştirilmelidir.

### C. Finans ve Burs (Cost & Scholarship Profile)
- **Eğitim Ücreti (Tuition):** "Düşük ücret" veya "Ücretsiz" gibi genel geçer ifadeler KABUL EDİLEMEZ. AB ve AB-dışı öğrenciler için net bölgesel harçlar, yönetim ücretleri dahil hesaplanmalı ve kaynak gösterilmelidir.
- **Burs Uygunluğu (Non-EU Eligibility):** Bursun uluslararası öğrencileri kapsayıp kapsamadığı teyit edilmelidir.
- **Yaşam Maliyeti:** Yurt, şehirdeki kira durumları araştırılmalı; burs miktarı yaşam maliyeti ile kıyaslanmalıdır.

### D. Araştırma ve Endüstri (Research & Industry Ecosystem)
- **Laboratuvarlar / Araştırma Merkezleri:** Programın ilgili alanındaki (CFD, GNC, İtki vb.) resmi araştırma gruplarının varlığı teyit edilmelidir.
- **Endüstri Bağlantıları:** Sadece staj ve tez süreçleri için resmi olarak adı geçen firmalar veya program sponsorları kaydedilmelidir.

---

## 4. ÖĞRENCİ HİSSİYATI (STUDENT SENTIMENT) KURALLARI

Öğrenci yorumları ASLA resmi bir gerçeklik olarak veritabanına işlenemez. Sadece aşağıdaki alanlarda algı/hissiyat sinyali olarak toplanabilir:
- Öğrenci Memnuniyet Skoru (student_satisfaction_score)
- İş Yükü (workload_sentiment)
- Yönetim / Öğrenci İşleri (administration_sentiment)
- Barınma Zorluğu (housing_sentiment)
- Kariyer Desteği (career_support_sentiment)

**Sentiment Toplama Kuralları:**
1. Tek bir olumlu veya olumsuz yoruma dayanarak genelleme yapma (Overfitting yasaktır).
2. Birbirinden bağımsız birden fazla kaynağı (Reddit, GradCafe vb.) tara.
3. Kaynakların güncelliğine dikkat et.
4. İfade edilen öğrenci görüşleri zayıf veya yetersizse `student_satisfaction_score` alanını `null` bırak, ve `sentiment_confidence` alanını `low` veya `unknown` yap. Skor uydurma.

---

## 5. GÜVEN DÜZEYİ (CONFIDENCE LEVEL) ATAMALARI

Her büyük veri grubu için (maliyet, burs, müfredat vb.) aşağıdaki yönergeye göre bir güven düzeyi (`confidence_level`) atanmalıdır:

- `high`: Resmi kaynak mevcut, bilgiler güncel, net ve doğrudan konuyla ilgili.
- `medium`: Resmi kaynak var ancak bilgiler eksik, yoruma açık, belirsiz veya güncelliği şüpheli.
- `low`: Sadece üçüncü parti kaynaklar, forumlar veya çok eski resmi olmayan veriler var. Doğrudan kanıt zayıf.
- `unknown`: Güvenilir hiçbir kaynağa ulaşılamadı.

---

## 6. AJAN İŞ AKIŞI STANDARDI (RESEARCH WORKFLOW)

Bir programı araştırmak üzere görevlendirildiğinde şu adımları TAVİZ VERMEDEN izle:

1. **Adayı Doğrula:** Program aktif mi? Kapanmış veya ismi değişmiş mi?
2. **Temel Parametreleri Çıkar:** Dil, Süre, ECTS.
3. **Kabul Şartlarını Netleştir:** Non-EU öğrencilerin başvuru süreçlerini ve ön koşulları (ECTS requirements) listele.
4. **Maliyetleri Teyit Et:** Harçlar ve burslar. Ulusal bursları (örn. İtalya) hesaba kat.
5. **Akademik Derinliği Ölç:** Müfredat (Zorunlu vs Seçmeli) ve araştırma laboratuvarlarını incele.
6. **Endüstri ve Kariyer:** Staj, tez imkanları, resmi partnerlikleri bul.
7. **Öğrenci Yorumlarını Topla:** Forum araştırması yapıp izole sentiment verisi oluştur.
8. **Güven Düzeylerini Ata:** Eksik alanları not et.
9. **Bağlantı (Link) Testi Yap:** Topladığın tüm kaynak URL'lerin erişilebilirliğini doğrula.
10. **JSON / Çıktı Oluştur:** Ancak yukarıdaki her şey eksiksiz yapıldıysa veya bilinmeyenler açıkça belirtildiyse veriyi kaydet.

---

## 7. ÇİFT DİLLİ VERİ (BILINGUAL DATA) KURALI

Agentlar tarafından üretilen JSON/Veri yapılarındaki anahtarlar (keys) daima **İngilizce** olmalıdır (örn. `tuition_eur_per_year`).
Ancak, kullanıcıya doğrudan sunulacak olan açıklama ve not metinleri **Çift Dilli** (İngilizce ve Türkçe) olmak zorundadır.

**Örnek:**
```json
{
  "en": "The program has strong industry ties with ESA, offering excellent thesis opportunities.",
  "tr": "Programın ESA ile güçlü endüstri bağları bulunmakta olup, mükemmel tez fırsatları sunmaktadır."
}
```

---

## 8. SON KONTROL VE DENETİM (CANARY TESTS)

Kayıt tamamlanmadan önce kendinize şu soruları sorun:
- Resmi olmayan bir kaynaktan alınmış finansal veri veya başvuru tarihi var mı? (Cevap EVET ise: SİL ve NULL yap)
- Bağlantılar 404 veriyor mu? (Cevap EVET ise: YENİ KAYNAK BUL veya BİLGİYİ İPTAL ET)
- "Galiba böyle", "Büyük ihtimalle" diye çıkarım yapılan bir veri var mı? (Cevap EVET ise: TAHMİNİ SİL)

**Bu kitapçıkta belirtilen yönergeler esnetilemez. UniRank platformunun kalitesi, eksik bile olsa sadece doğrulanmış bilgiye sahip olmasına bağlıdır. Yanlış veri, eksik veriden çok daha zararlıdır.**
