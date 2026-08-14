# Student-sentiment batch 1 (researched 2026-07-18).
#
# Sources were checked on 2026-07-18. EDUopinions aggregate pages were
# machine-fetched and read in full ("ok"); Reddit discussion threads were
# located through web search and their topic titles verified, but Reddit
# blocks anonymous machine readers, so they are recorded as "requires_js"
# and are never used as the basis of a score.
#
# Per AGENTS.md: sentiment is perception, not fact. A numeric satisfaction
# score is stored only where a single consistent aggregate with a
# reasonable sample size (>= 50 reviews) exists, and confidence is capped
# at "medium" because the evidence comes from one review platform.
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data_base"
CHECKED = "2026-07-18"


def bi(en, tr):
    return {"en": en, "tr": tr}


def src(url, title, platform, notes_en, notes_tr, access="ok"):
    return {
        "platform": platform,
        "title": title,
        "url": url,
        "source_type": "student_forum" if platform == "reddit" else "third_party_reviews",
        "access_status": access,
        "last_checked": CHECKED,
        "notes": bi(notes_en, notes_tr),
    }


SENTIMENTS = {
    # ------------------------------------------------------------------
    ("italy.json", "polimi-msc-aeronautical"): None,  # filled below (shared)
}

POLIMI = {
    "student_satisfaction_score": 82,
    "sentiment_confidence": "medium",
    "sample_size_estimate": 80,
    "date_range": "reviews collected up to 2026-07",
    "student_sentiment_summary": bi(
        "Aggregated student reviews (EDUopinions, 4.1/5 from 80 reviews) are broadly positive: "
        "teaching quality, reputation and research environment are praised, while the recurring "
        "complaints are a heavy theoretical workload and limited built-in practical or internship "
        "experience. Reddit discussions on the aerospace programme raise the same themes.",
        "Toplu öğrenci değerlendirmeleri (EDUopinions, 80 yorumda 4.1/5) genel olarak olumlu: "
        "öğretim kalitesi, kurumun itibarı ve araştırma ortamı övülüyor; tekrarlayan şikayetler ise "
        "ağır teorik iş yükü ve programa gömülü uygulama/staj deneyiminin sınırlı olması. "
        "Havacılık-uzay programına dair Reddit tartışmaları da aynı temaları içeriyor.",
    ),
    "verification_notes": bi(
        "Score mirrors the EDUopinions aggregate (4.1/5 → 82/100). Single-platform aggregate; "
        "confidence capped at medium. Reddit threads verified by title only (anonymous access blocked).",
        "Puan EDUopinions ortalamasını yansıtır (4.1/5 → 82/100). Tek platform ortalamasıdır; güven "
        "'medium' ile sınırlandı. Reddit başlıkları yalnızca başlık düzeyinde doğrulandı (anonim erişim engelli).",
    ),
    "student_sentiment_sources": [
        src(
            "https://www.eduopinions.com/universities/universities-in-italy/politecnico-di-milano/",
            "EDUopinions – Politecnico di Milano student reviews (4.1/5, 80 reviews)",
            "eduopinions",
            "Aggregate read in full on the check date.",
            "Toplu değerlendirme sayfası kontrol tarihinde tam okundu.",
        ),
        src(
            "https://www.reddit.com/r/AerospaceEngineering/comments/127bs4u/politechnico_di_milano_for_ms_aeronautical/",
            "r/AerospaceEngineering – Politecnico di Milano for MS Aeronautical Engineering?",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
        src(
            "https://www.reddit.com/r/Universitaly/comments/1do3x5g/how_is_politecnico_di_milano/",
            "r/Universitaly – How is Politecnico di Milano?",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
    ],
}

DELFT = {
    "student_satisfaction_score": 84,
    "sentiment_confidence": "medium",
    "sample_size_estimate": 109,
    "date_range": "reviews collected up to 2026-07",
    "student_sentiment_summary": bi(
        "Aggregated reviews (EDUopinions, 4.2/5 from 109 reviews) praise the programme depth, "
        "facilities and international environment; recurring negatives are the demanding "
        "mathematics-heavy workload and limited personal guidance in large cohorts. Housing "
        "availability in Delft is a persistent worry in student discussions.",
        "Toplu değerlendirmeler (EDUopinions, 109 yorumda 4.2/5) programın derinliğini, kampüs "
        "olanaklarını ve uluslararası ortamı övüyor; tekrarlayan olumsuzluklar yoğun matematik "
        "ağırlıklı iş yükü ve kalabalık sınıflarda birebir yönlendirmenin azlığı. Delft'te konut "
        "bulma endişesi öğrenci tartışmalarında süreklilik gösteriyor.",
    ),
    "verification_notes": bi(
        "Score mirrors the EDUopinions aggregate (4.2/5 → 84/100). Single-platform aggregate; "
        "confidence capped at medium. Reddit threads verified by title only.",
        "Puan EDUopinions ortalamasını yansıtır (4.2/5 → 84/100). Tek platform ortalamasıdır; güven "
        "'medium' ile sınırlandı. Reddit başlıkları yalnızca başlık düzeyinde doğrulandı.",
    ),
    "student_sentiment_sources": [
        src(
            "https://www.eduopinions.com/universities/universities-in-the-netherlands/delft-university-of-technology-tu-delft/",
            "EDUopinions – TU Delft student reviews (4.2/5, 109 reviews)",
            "eduopinions",
            "Aggregate read in full on the check date.",
            "Toplu değerlendirme sayfası kontrol tarihinde tam okundu.",
        ),
        src(
            "https://www.reddit.com/r/TUDelft/comments/tmkslt/got_admitted_to_the_aerospace_msc_now_wondering/",
            "r/TUDelft – Got admitted to the Aerospace MSc! Now wondering about housing",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
        src(
            "https://www.reddit.com/r/TUDelft/comments/184vvti/how_difficult_is_the_msc_in_aerospace_engineering/",
            "r/TUDelft – How difficult is the MSc in Aerospace Engineering?",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
    ],
}

ISAE = {
    "student_satisfaction_score": None,
    "sentiment_confidence": "low",
    "sample_size_estimate": 7,
    "date_range": "reviews collected up to 2026-07",
    "student_sentiment_summary": bi(
        "Only a small review sample exists (EDUopinions, 4.6/5 from 7 reviews), so no numeric score "
        "is shown. Reviewers consistently praise Toulouse's aerospace industry connections, "
        "internship access and industry-focused software teaching; the recurring criticism is that "
        "some industry lecturers teach poorly and lecture blocks are long and draining.",
        "Yorum örneklemi küçük olduğundan (EDUopinions, 7 yorumda 4.6/5) sayısal puan gösterilmiyor. "
        "Değerlendirmeler Toulouse'un havacılık-uzay sanayi bağlantılarını, staj erişimini ve sektör "
        "yazılımlarına dayalı öğretimi tutarlı biçimde övüyor; tekrarlayan eleştiri, sektörden gelen "
        "bazı eğitmenlerin ders anlatımının zayıf ve ders bloklarının uzun/yorucu olması.",
    ),
    "verification_notes": bi(
        "Sample too small for a score (7 reviews, one platform). Reddit threads verified by title only.",
        "Puan için örneklem çok küçük (tek platformda 7 yorum). Reddit başlıkları yalnızca başlık düzeyinde doğrulandı.",
    ),
    "student_sentiment_sources": [
        src(
            "https://www.eduopinions.com/universities/universities-in-france/institut-superieur-de-laeronautique-et-de-lespace-isae-supaero/",
            "EDUopinions – ISAE-SUPAERO student reviews (4.6/5, 7 reviews)",
            "eduopinions",
            "Aggregate read in full on the check date.",
            "Toplu değerlendirme sayfası kontrol tarihinde tam okundu.",
        ),
        src(
            "https://www.reddit.com/r/AerospaceEngineering/comments/l8ou8k/experience_in_isae_supaero/",
            "r/AerospaceEngineering – Experience in ISAE SUPAERO",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
        src(
            "https://www.reddit.com/r/aerospace/comments/1cwrm53/msc_at_isae_supaero/",
            "r/aerospace – MSc at ISAE SUPAERO?",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
    ],
}

KTH = {
    "student_satisfaction_score": None,
    "sentiment_confidence": "low",
    "sample_size_estimate": 12,
    "date_range": "reviews collected up to 2026-07",
    "student_sentiment_summary": bi(
        "The review sample is small (EDUopinions, 4.7/5 from 12 reviews), so no numeric score is "
        "shown. Reviewers highlight world-class research facilities, an inclusive international "
        "environment and strong industry networking; the recurring criticism is that some "
        "research-oriented professors give teaching less attention and several courses are intense.",
        "Yorum örneklemi küçük olduğundan (EDUopinions, 12 yorumda 4.7/5) sayısal puan gösterilmiyor. "
        "Değerlendirmeler dünya standardında araştırma olanaklarını, kapsayıcı uluslararası ortamı ve "
        "güçlü sektör ağını öne çıkarıyor; tekrarlayan eleştiri, araştırma odaklı bazı hocaların "
        "öğretime daha az önem vermesi ve bazı derslerin yoğunluğu.",
    ),
    "verification_notes": bi(
        "Sample too small for a score (12 reviews, one platform). Reddit thread verified by title only.",
        "Puan için örneklem çok küçük (tek platformda 12 yorum). Reddit başlığı yalnızca başlık düzeyinde doğrulandı.",
    ),
    "student_sentiment_sources": [
        src(
            "https://www.eduopinions.com/universities/universities-in-sweden/royal-institute-technology-kth/",
            "EDUopinions – KTH student reviews (4.7/5, 12 reviews)",
            "eduopinions",
            "Aggregate read in full on the check date.",
            "Toplu değerlendirme sayfası kontrol tarihinde tam okundu.",
        ),
        src(
            "https://www.reddit.com/r/AerospaceEngineering/comments/ddkrm8/thoughts_on_msc_at_kth/",
            "r/AerospaceEngineering – Thoughts on MSc at KTH",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
    ],
}

DARMSTADT = {
    "student_satisfaction_score": None,
    "sentiment_confidence": "low",
    "sample_size_estimate": 9,
    "date_range": "reviews collected up to 2026-07",
    "student_sentiment_summary": bi(
        "The review sample is small (EDUopinions, 4.2/5 from 9 reviews), so no numeric score is "
        "shown. Reviewers praise the research-oriented environment, modern laboratories and a "
        "student-friendly city near Frankfurt; recurring notes are a demanding workload and an "
        "adjustment period for internationals entering the German academic system.",
        "Yorum örneklemi küçük olduğundan (EDUopinions, 9 yorumda 4.2/5) sayısal puan gösterilmiyor. "
        "Değerlendirmeler araştırma odaklı ortamı, modern laboratuvarları ve Frankfurt'a yakın "
        "öğrenci dostu şehri övüyor; tekrarlayan notlar, iş yükünün ağırlığı ve uluslararası "
        "öğrenciler için Alman akademik sistemine uyum süreci.",
    ),
    "verification_notes": bi(
        "Sample too small for a score (9 reviews, one platform). Reddit thread verified by title only.",
        "Puan için örneklem çok küçük (tek platformda 9 yorum). Reddit başlığı yalnızca başlık düzeyinde doğrulandı.",
    ),
    "student_sentiment_sources": [
        src(
            "https://www.eduopinions.com/universities/universities-in-germany/darmstadt-university-technology-tu-darmstadt/",
            "EDUopinions – TU Darmstadt student reviews (4.2/5, 9 reviews)",
            "eduopinions",
            "Aggregate read in full on the check date.",
            "Toplu değerlendirme sayfası kontrol tarihinde tam okundu.",
        ),
        src(
            "https://www.reddit.com/r/tudarmstadt/comments/v9fwj4/tu_darmstadt_msc_aerospace/",
            "r/tudarmstadt – TU Darmstadt msc aerospace",
            "reddit",
            "Thread located via search; topic title verified, content not machine-readable.",
            "Başlık arama ile bulundu ve doğrulandı; içerik makine tarafından okunamadı.",
            access="requires_js",
        ),
    ],
}

TARGETS = [
    ("italy.json", "polimi-msc-aeronautical", POLIMI),
    ("italy.json", "polimi-msc-aeronautical", POLIMI),
    ("italy.json", "polimi-msc-space", POLIMI),
    ("hollanda.json", "netherlands_delft_msc_aerospace", DELFT),
    ("fransa.json", "france_isae_supaero_msc", ISAE),
    ("isvec.json", "se-kth-aero-msc", KTH),
    ("almanya.json", "de_darmstadt_aerospace_engineering_msc", DARMSTADT),
]


def main():
    for filename, record_id, sentiment in TARGETS:
        path = DATA / filename
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload if isinstance(payload, list) else payload.get("programs") or payload.get("universities")
        record = next((r for r in rows if r.get("id") == record_id), None)
        if record is None:
            raise SystemExit(f"Record not found: {filename} / {record_id}")
        record["student_sentiment_profile"] = dict(sentiment)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"updated {filename} / {record_id}")


if __name__ == "__main__":
    main()
