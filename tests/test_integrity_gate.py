from unirank.core.integrity import apply_integrity_gate, audit_record


def checked_source(source_type, fields):
    return {
        "url": "https://example.edu/source",
        "source_type": source_type,
        "access_status": "ok",
        "relevant_fields": fields,
    }


def test_integrity_gate_hides_unsupported_decision_values():
    record = {
        "teaching_language": ["English"],
        "cost_profile": {"tuition_eur_per_year_estimated": 9999},
        "living_profile": {"average_room_rent_eur": 900},
        "student_sentiment_profile": {"student_satisfaction_score": 92},
        "source_profile": {"source_log": [checked_source("official_program_page", ["program"]) ]},
    }

    gated = apply_integrity_gate(record)

    assert gated["teaching_language"] == ["Unknown"]
    assert gated["cost_profile"]["tuition_eur_per_year_estimated"] is None
    assert gated["living_profile"]["average_room_rent_eur"] is None
    assert gated["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert gated["data_quality"]["status"] == "partial"


def test_integrity_audit_accepts_checked_direct_sources_only():
    record = {
        "source_profile": {
            "source_log": [
                checked_source("official_program_page", ["program", "language"]),
                checked_source("official_tuition_page", ["tuition"]),
                checked_source("official_scholarship_page", ["scholarship"]),
                checked_source("official_curriculum_page", ["curriculum"]),
                checked_source("official_admission_page", ["admission"]),
                {"url": "https://forum.example", "source_type": "student_forum", "access_status": "ok"},
            ]
        }
    }

    quality = audit_record(record)
    assert quality["status"] == "verified"
    assert quality["checked_official_source_count"] == 5
