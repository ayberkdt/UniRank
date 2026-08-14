import json
from pathlib import Path

from unirank.core.json_loader import load_database_folder


ROOT = Path(__file__).resolve().parents[1]
EUROPE = {
    "almanya.json", "austria.json", "belcika.json", "cekya.json", "danimarka.json",
    "finlandiya.json", "fransa.json", "hollanda.json", "ingiltere.json", "ispanya.json",
    "isvec.json", "isvicre.json", "italy.json", "polonya.json",
    "portekiz.json", "turkiye.json", "yunanistan.json",
}


def records(path: Path):
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(value, dict):
        return value.get("universities") or value.get("programs") or []
    return value


def test_every_europe_record_has_sourced_qs_2027_profile():
    for filename in EUROPE:
        for record in records(ROOT / "data_base" / filename):
            qs = record["ranking_profile"]["qs_world_university_rankings"]
            assert qs["edition"] == 2027
            assert qs["source_url"].startswith("https://www.topuniversities.com/")
            assert qs["last_checked"] == "2026-07-19"
            assert qs["technical_fit_use"] is False
            if qs["status"] == "ranked":
                assert qs["display_rank"]
                if qs["rank_type"] == "band":
                    assert record["qs_ranking"] is None


def test_known_bad_legacy_values_are_replaced():
    anchors = {
        "Delft University of Technology": "48",
        "University of Cambridge": "6",
        "University of Oxford": "4",
        "Technical University of Munich": "25",
        "Istanbul Technical University (ITU)": "=279",
    }
    found = {}
    for filename in EUROPE:
        for record in records(ROOT / "data_base" / filename):
            name = record.get("university")
            if name in anchors:
                found[name] = record["qs_ranking_display"]
    assert found == anchors


def test_loader_exposes_rank_display_and_profile():
    frame, _ = load_database_folder(ROOT / "data_base", strict=False)
    delft = frame[frame["university"] == "Delft University of Technology"].iloc[0]
    assert delft["qs_ranking"] == 48
    assert delft["qs_ranking_display"] == "48"
    assert delft["qs_ranking_year"] == 2027
    assert delft["ranking_profile"]["qs_world_university_rankings"]["source_type"] == "official_qs"
