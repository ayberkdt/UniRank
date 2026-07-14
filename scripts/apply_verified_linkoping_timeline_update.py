"""Replace an ambiguous Linköping deadline label with the checked official cycle."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apply_verified_polimi_aero_update import bi, source


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data_base" / "isvec.json"
CHECKED = "2026-07-14"


def main() -> None:
    original = PATH.read_text(encoding="utf-8")
    document: list[dict[str, Any]] = json.loads(original)
    row = next(item for item in document if item.get("id") == "se-linkoping-aero-msc")
    application_url = "https://liu.se/en/education/application-and-admission/how-to-apply"

    row["application_timeline_profile"] = {
        "academic_year": "2026/2027 closed reference cycle; next-cycle dates not yet published on the checked page",
        "intake_terms": ["autumn; Master's programmes start in August"],
        "application_rounds": ["International Master's application submission: 15 January 2026", "Supporting documents and application fee: 2 February 2026", "Selection result: 26 March 2026", "LiU scholarship period: 26-31 March 2026"],
        "non_eu_deadline": "2026-01-15 (application); 2026-02-02 (supporting documents and application fee)",
        "eu_deadline": "2026-01-15 (international Master's application round)",
        "winter_deadline": None,
        "summer_deadline": None,
        "application_deadline": "2026-01-15 for the checked 2026/27 international Master's round",
        "scholarship_deadline": "2026-03-31 for the checked LiU scholarship period",
        "timeline_risk": "high",
        "deadline_notes": bi("The official LiU page currently publishes the closed 2026/27 international Master's cycle, not an exact 2027/28 date. The record shows that checked cycle for planning context and deliberately refuses to extrapolate it. An applicant for the next intake must use the programme's Apply button/University Admissions when the new round opens.", "Resmî LiU sayfası şu anda kesin 2027/28 tarihi değil, kapanmış 2026/27 uluslararası yüksek lisans döngüsünü yayımlar. Kayıt bu doğrulanmış döngüyü planlama bağlamı için gösterir ve geleceğe taşımayı kasıtlı olarak reddeder. Sonraki girişe başvuracak aday, yeni dönem açıldığında programın Apply düğmesini/University Admissions sistemini kullanmalıdır."),
    }
    profile = row.setdefault("source_profile", {})
    logs = [item for item in profile.get("source_log", []) if isinstance(item, dict) and item.get("url") != application_url]
    logs.append(source(application_url, "How to apply for Master's degree studies at LiU", "official_admission_page", ["admission", "deadline", "non_eu", "scholarship"], "Current LiU guide documents the 15 January 2026 application deadline, 2 February document/fee deadline, 26 March Master's result and 26-31 March scholarship period for the checked international Master's cycle, and explains that no Master's programmes start in spring.", "Güncel LiU rehberi, kontrol edilen uluslararası yüksek lisans döngüsü için 15 Ocak 2026 başvuru son tarihini, 2 Şubat belge/ücret son tarihini, 26 Mart yüksek lisans sonucunu ve 26-31 Mart burs dönemini belgeler; ayrıca yüksek lisans programlarının baharda başlamadığını açıklar."))
    profile.update({
        "official_admission_page": application_url,
        "source_log": logs,
        "last_verified": CHECKED,
        "needs_verification": False,
    })
    profile.setdefault("field_confidence", {})["application_timeline_profile"] = "high"
    document_text = json.dumps(document, ensure_ascii=False, indent=2)
    newline = "\r\n" if "\r\n" in original else "\n"
    PATH.write_text(document_text.replace("\n", newline) + newline, encoding="utf-8")
    print("Updated Linköping Aeronautical Engineering with the checked official application cycle.")


if __name__ == "__main__":
    main()
