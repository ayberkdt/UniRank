import json

from api.index import (
    _database_records,
    _institutional_funding,
    _programme_research_details,
    get_universities,
)


def test_scholarship_api_exposes_programme_playbooks():
    profiles = _institutional_funding(_database_records())

    assert profiles
    assert all(profile["playbook"] for profile in profiles)
    assert any(profile["featured"] for profile in profiles)
    assert all(
        opportunity.get("evidence_url")
        for profile in profiles
        for opportunity in profile["playbook"]
    )


def test_research_api_exposes_faculty_and_laboratory_evidence():
    profiles = _programme_research_details(_database_records())

    assert profiles
    assert any(profile["notable_professors"] for profile in profiles)
    assert any(profile["research_units"] for profile in profiles)
    assert any(profile["featured"] for profile in profiles)


def test_faculty_email_is_never_exposed_without_official_email_source():
    profiles = _programme_research_details(_database_records())

    assert all(
        not professor.get("email") or professor.get("email_source")
        for profile in profiles
        for professor in profile["notable_professors"]
    )


def test_featured_profiles_sort_before_other_profiles():
    scholarship_profiles = _institutional_funding(_database_records())
    research_profiles = _programme_research_details(_database_records())

    for profiles in (scholarship_profiles, research_profiles):
        flags = [profile["featured"] for profile in profiles]
        assert flags == sorted(flags, reverse=True)


def test_university_api_supports_bounded_progressive_pages():
    response = get_universities(limit=7, offset=3)
    payload = json.loads(response.body)

    assert payload["status"] == "success"
    assert len(payload["data"]) == 7
    assert payload["page"]["offset"] == 3
    assert payload["page"]["limit"] == 7
    assert payload["page"]["total"] >= 10
    assert payload["page"]["next_offset"] == 10
