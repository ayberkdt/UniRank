"""Apply source-checked QS World University Rankings 2027 metadata to Europe.

Legacy ``qs_ranking`` values had no edition/source and mixed exact ranks with
unsupported numbers. This migration keeps the numeric field only for exact
ranks and preserves ties and rank bands in ``qs_ranking_display``.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_base"
VERIFIED_ON = "2026-07-19"
EDITION = 2027
TABLE_URL = "https://www.topuniversities.com/world-university-rankings"

EUROPE_FILES = {
    "almanya.json", "austria.json", "belcika.json", "cekya.json",
    "danimarka.json", "finlandiya.json", "fransa.json", "hollanda.json",
    "ingiltere.json", "ispanya.json", "isvec.json", "isvicre.json",
    "italy.json", "polonya.json", "portekiz.json",
    "turkiye.json", "yunanistan.json",
}


def ranked(display: str, slug: str | None = None, *, parent: str | None = None) -> dict:
    clean = display.removeprefix("=")
    exact = clean.isdigit()
    return {
        "display": display,
        "numeric": int(clean) if exact else None,
        "sort_rank": int(clean.split("-")[0]) if clean.split("-")[0].isdigit() else None,
        "rank_type": "exact" if exact else "band",
        "source": f"https://www.topuniversities.com/universities/{slug}" if slug else TABLE_URL,
        "ranked_institution": parent,
    }


# Keys are the exact institution labels present in the database. Parent matches
# are explicit so a faculty/school is not presented as independently ranked.
RANKS = {
    # Germany
    "Technical University of Munich": ranked("25", "technical-university-munich"),
    "University of Stuttgart": ranked("=318", "universitat-stuttgart"),
    "Karlsruhe Institute of Technology (KIT)": ranked("110", "kit-karlsruhe-institute-technology"),
    "TU Braunschweig": ranked("781-790", "technische-universitat-braunschweig"),
    "TU Berlin": ranked("=158", "technische-universitat-berlin-tu-berlin"),
    "Universität Bremen": ranked("=581", "universitat-bremen"),
    "TU Darmstadt": ranked("250", "technical-university-darmstadt"),
    "RWTH Aachen University": ranked("104", "rwth-aachen-university"),
    "Hamburg University of Technology (TUHH)": ranked("721-730", "tuhh-hamburg-university-technology"),

    # Austria
    "TU Graz": ranked("=409", "graz-university-technology"),
    "TU Wien": ranked("=191", "technische-universitat-wien"),
    "University of Innsbruck": ranked("333", "universitat-innsbruck"),
    "Johannes Kepler University Linz (JKU)": ranked("=458", "johannes-kepler-university-linz"),
    "Montanuniversität Leoben": ranked("851-900", "montanuniversitat-leoben"),

    # Belgium
    "KU Leuven": ranked("59"),
    "University of Liège (ULiège)": ranked("=364", "universite-de-liege"),
    "Ghent University (UGent)": ranked("=150"),
    "Vrije Universiteit Brussel (VUB)": ranked("295", "vrije-universiteit-brussel-vub"),
    "Université libre de Bruxelles (ULB)": ranked("248", "universite-libre-de-bruxelles"),
    "UCLouvain (Université catholique de Louvain)": ranked("=196"),
    "University of Antwerp": ranked("=277", "university-antwerp"),
    "University of Mons (UMons)": ranked("801-850", "university-mons"),
    "University of Namur (UNamur)": ranked("801-850", "university-namur"),

    # Czechia, Denmark, Finland, France
    "Czech Technical University in Prague": ranked("=432", "czech-technical-university-prague"),
    "Brno University of Technology": ranked("=588", "brno-university-technology"),
    "Technical University of Denmark (DTU)": ranked("105"),
    "Aalto University": ranked("=126"),
    "Université Paris-Saclay (Université d'Évry)": ranked("76", parent="Université Paris-Saclay"),

    # Netherlands
    "Delft University of Technology": ranked("48"),
    "Eindhoven University of Technology": ranked("152"),
    "University of Twente": ranked("=223", "university-twente"),

    # United Kingdom
    "University of Cambridge": ranked("6"),
    "Imperial College London": ranked("=2"),
    "University of Oxford": ranked("4"),
    "University College London (UCL)": ranked("=8"),
    "The University of Manchester": ranked("=40"),
    "University of Southampton": ranked("=111"),
    "University of Bristol": ranked("57"),
    "University of Leeds": ranked("=77"),
    "University of Sheffield": ranked("=82"),
    "University of Glasgow": ranked("80"),
    "University of Liverpool": ranked("139"),
    "The University of Edinburgh": ranked("35"),
    "University of Birmingham": ranked("=68"),
    "University of Nottingham": ranked("97"),
    "University of Surrey": ranked("=246", "university-surrey"),

    # Spain
    "Universidad Politécnica de Madrid": ranked("=364", "universidad-politecnica-de-madrid-upm"),
    "Universitat Politècnica de Catalunya": ranked("=434", "universitat-politecnica-de-catalunya-barcelonatech-upc"),
    "Universidad Carlos III de Madrid": ranked("=314", "universidad-carlos-iii-de-madrid-uc3m"),

    # Sweden, Switzerland
    "KTH Royal Institute of Technology": ranked("=82"),
    "Chalmers University of Technology": ranked("=174"),
    "Linköping University": ranked("308", "linkoping-university"),
    "ETH Zurich": ranked("=8"),
    "EPFL (École Polytechnique Fédérale de Lausanne)": ranked("=22"),
    "ZHAW Zurich University of Applied Sciences": ranked("851-900", "zurich-university-applied-sciences-zhaw"),

    # Italy (both source files use these aliases)
    "Politecnico di Milano": ranked("=87"),
    "Politecnico di Torino": ranked("=206", "politecnico-di-torino"),
    "Sapienza University of Rome": ranked("=111"),
    "University of Bologna": ranked("=123"),
    "University of Padova": ranked("204", "universita-di-padova"),
    "University of Padua": ranked("204", "universita-di-padova"),
    "University of Pisa": ranked("341", "university-pisa"),
    "University of Naples Federico II": ranked("401", "university-naples-federico-ii"),
    "Politecnico di Bari": ranked("951-1000", "politecnico-di-bari"),
    "Università del Salento": ranked("1001-1200", "university-salento"),
    "Università di Palermo": ranked("801-850", "university-palermo"),
    "University of Palermo": ranked("801-850", "university-palermo"),
    "University of Trento": ranked("=438", "university-trento"),

    # Poland
    "Warsaw University of Technology": ranked("=504", "warsaw-university-technology"),
    "AGH University of Science and Technology": ranked("761-770", "agh-university-krakow"),
    "Wrocław University of Science and Technology": ranked("901-950", "wroclaw-university-science-technology-wroclaw-tech"),
    "Silesian University of Technology": ranked("1001-1200", "silesian-university-technology"),
    "Gdańsk University of Technology": ranked("801-850", "gdansk-university-technology"),

    # Portugal; schools inherit only the parent institution's global rank.
    "Instituto Superior Técnico (Técnico Lisboa)": ranked("=237", "university-lisbon", parent="University of Lisbon"),
    "University of Porto (FEUP)": ranked("=255", "university-porto", parent="University of Porto"),
    "University of Aveiro": ranked("=425", "university-aveiro"),
    "University of Minho": ranked("=572", "university-minho"),
    "NOVA School of Science and Technology (FCT NOVA)": ranked("337", "universidade-nova-de-lisboa", parent="Universidade Nova de Lisboa"),

    # Türkiye
    "Istanbul Technical University (ITU)": ranked("=279", "istanbul-technical-university"),
    "Middle East Technical University (METU)": ranked("305", "middle-east-technical-university"),
    "Boğaziçi University": ranked("=345", "bogazici-university"),

    # Greece
    "Aristotle University of Thessaloniki": ranked("=502", "aristotle-university-thessaloniki"),
    "University of Patras": ranked("771-780", "university-patras"),
    "National and Kapodistrian University of Athens": ranked("=402", "national-kapodistrian-university-athens"),
}


def university_name(record: dict) -> str:
    return str(record.get("university") or record.get("University_Name") or "").strip()


def apply_record(record: dict) -> tuple[bool, str]:
    name = university_name(record)
    value = RANKS.get(name)
    record.pop("QS_Ranking", None)
    if value:
        ranked_institution = value["ranked_institution"] or name
        record["qs_ranking"] = value["numeric"]
        record["qs_ranking_display"] = value["display"]
        record["qs_ranking_year"] = EDITION
        record["ranking_profile"] = {
            "qs_world_university_rankings": {
                "edition": EDITION,
                "status": "ranked",
                "rank": value["numeric"],
                "display_rank": value["display"],
                "rank_type": value["rank_type"],
                "sort_rank": value["sort_rank"],
                "ranked_institution": ranked_institution,
                "match_type": "parent_university" if value["ranked_institution"] else "direct",
                "source_url": value["source"],
                "source_type": "official_qs",
                "access_status": "ok",
                "published_on": "2026-06-18",
                "last_checked": VERIFIED_ON,
                "confidence": "high",
                "technical_fit_use": False,
                "notes": {
                    "en": "Institutional global rank; it is not evidence of aerospace or space-programme fit.",
                    "tr": "Kurumsal dünya sıralamasıdır; havacılık veya uzay programı uygunluğunun kanıtı değildir.",
                },
            }
        }
        return True, name

    # Unknown is safer than retaining an unsourced legacy number.
    record["qs_ranking"] = None
    record["qs_ranking_display"] = None
    record["qs_ranking_year"] = EDITION
    record["ranking_profile"] = {
        "qs_world_university_rankings": {
            "edition": EDITION,
            "status": "not_verified",
            "rank": None,
            "display_rank": None,
            "rank_type": None,
            "sort_rank": None,
            "ranked_institution": name,
            "match_type": "unresolved",
            "source_url": TABLE_URL,
            "source_type": "official_qs",
            "access_status": "ok",
            "published_on": "2026-06-18",
            "last_checked": VERIFIED_ON,
            "confidence": "unknown",
            "technical_fit_use": False,
            "notes": {
                "en": "No independent 2027 QS WUR rank was verified for this database institution; no value is inferred.",
                "tr": "Bu veri tabanı kurumu için bağımsız bir 2027 QS WUR sırası doğrulanmadı; değer türetilmedi.",
            },
        }
    }
    return False, name


def main() -> None:
    ranked_count = 0
    unknown_names: set[str] = set()
    record_count = 0
    for filename in sorted(EUROPE_FILES):
        path = DATA / filename
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        records = payload
        if isinstance(payload, dict):
            key = "universities" if isinstance(payload.get("universities"), list) else "programs"
            records = payload[key]
        for record in records:
            ok, name = apply_record(record)
            ranked_count += int(ok)
            record_count += 1
            if not ok:
                unknown_names.add(name)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated {record_count} European programme records; {ranked_count} received verified QS 2027 ranks.")
    print("Not verified as independent QS WUR institutions:")
    for name in sorted(unknown_names):
        print(f"- {name}")


if __name__ == "__main__":
    main()
