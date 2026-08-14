"""Move Edinburgh's no-program placeholder out of the programme catalogue."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UK_PATH = ROOT / "data_base" / "ingiltere.json"
QUEUE_PATH = ROOT / "research_queue" / "program_candidates_v2.json"
RECORD_ID = "university-of-edinburgh"
CHECKED = "2026-08-14"
TAUGHT_CATALOGUE = "https://study.ed.ac.uk/programmes/postgraduate-subjects/engineering"
SCHOOL_LIST = "https://eng.ed.ac.uk/discover-postgraduate-engineering"
RESEARCH_CATALOGUE = "https://study.ed.ac.uk/programmes/postgraduate-research/947-engineering"


def bi(en: str, tr: str) -> dict[str, str]:
    return {"en": en, "tr": tr}


def main() -> None:
    rows = json.loads(UK_PATH.read_text(encoding="utf-8"))
    matches = [row for row in rows if row.get("id") == RECORD_ID]
    if len(matches) > 1:
        raise RuntimeError(f"Expected at most one {RECORD_ID!r}; found {len(matches)}")
    if matches:
        row = matches[0]
        if not str(row.get("program_name") or "").startswith("No dedicated taught"):
            raise RuntimeError("Refusing to retire a real Edinburgh programme record")
        rows.remove(row)

    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    candidate = {
        "candidate_id": "uk-edinburgh-no-dedicated-aerospace-space-masters",
        "country": "United Kingdom",
        "institution": "The University of Edinburgh",
        "program_name": None,
        "degree_level": "Master",
        "official_program_url": TAUGHT_CATALOGUE,
        "discovery_status": "excluded_no_eligible_program",
        "relevance_basis": [],
        "priority": "none",
        "catalogue_scope": "2026 postgraduate Engineering taught and named research awards",
        "catalogue_programmes_checked": [
            "Advanced Chemical Engineering MSc",
            "Advanced Power Engineering MSc",
            "Biomedical Engineering MSc",
            "Digital Design and Manufacture MSc",
            "Electrical Power Engineering MSc",
            "Electronics MSc",
            "Fire Engineering Science MSc",
            "International Master of Science in Fire Safety Engineering MSc",
            "Sensor and Imaging Systems MSc",
            "Signal Processing and Communications MSc",
            "Sustainable Energy Systems MSc",
        ],
        "evidence_summary": bi(
            "The current official Engineering taught-programme catalogue and School list contain no Aerospace, Aeronautical, Astronautics, Space Engineering or dedicated Space Systems master's. The generic Engineering research page offers MPhil and PhD study options, not an MScR award. Edinburgh is therefore retained as a checked institutional exclusion rather than represented by a fabricated programme pair.",
            "Güncel resmî Mühendislik taught-program kataloğu ve Fakülte listesinde Aerospace, Aeronautical, Astronautics, Space Engineering veya özel Space Systems yüksek lisansı yoktur. Genel Engineering araştırma sayfası MScR değil MPhil ve PhD seçenekleri sunar. Bu nedenle Edinburgh uydurma bir program çiftiyle gösterilmek yerine kontrol edilmiş kurumsal dışlama olarak tutulur.",
        ),
        "known_cautions": [
            bi(
                "Sensor and Imaging Systems mentions aerospace as one possible employment market, but that does not make it an aerospace or space-engineering degree.",
                "Sensor and Imaging Systems, havacılığı olası istihdam pazarlarından biri olarak anar; bu durum programı havacılık veya uzay mühendisliği derecesi yapmaz.",
            ),
            bi(
                "Institutional prestige and engineering research reputation must not be converted into programme fit.",
                "Kurumsal prestij ve mühendislik araştırma itibarı program uygunluğuna dönüştürülmemelidir.",
            ),
        ],
        "discovery_sources": [
            {
                "url": TAUGHT_CATALOGUE,
                "source_type": "official_university_catalogue",
                "title": "University of Edinburgh postgraduate Engineering subject catalogue",
                "access_status": "ok",
                "last_checked": CHECKED,
                "confidence": "high",
                "relevant_fields": ["taught_programme_catalogue", "programme_availability"],
            },
            {
                "url": SCHOOL_LIST,
                "source_type": "official_department_page",
                "title": "University of Edinburgh discover postgraduate Engineering",
                "access_status": "ok",
                "last_checked": CHECKED,
                "confidence": "high",
                "relevant_fields": ["taught_programme_catalogue"],
            },
            {
                "url": RESEARCH_CATALOGUE,
                "source_type": "official_program_page",
                "title": "University of Edinburgh Engineering PhD and MPhil",
                "access_status": "ok",
                "last_checked": CHECKED,
                "confidence": "high",
                "relevant_fields": ["research_awards", "programme_availability"],
            },
        ],
        "discovery_source": {
            "source_type": "official_university_catalogue",
            "access_status": "ok",
            "last_checked": CHECKED,
        },
        "last_verified": CHECKED,
        "next_review_trigger": "Re-run when the University publishes the 2027/28 Engineering catalogue or announces a new aerospace/space master's.",
    }
    candidates = queue["candidates"]
    existing = [
        item for item in candidates if item.get("candidate_id") == candidate["candidate_id"]
    ]
    if len(existing) > 1:
        raise RuntimeError("Duplicate Edinburgh exclusion candidates")
    if existing:
        existing[0].clear()
        existing[0].update(candidate)
    else:
        candidates.append(candidate)
    queue["last_updated"] = CHECKED

    UK_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    QUEUE_PATH.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
