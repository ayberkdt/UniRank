import json
from pathlib import Path

import pandas as pd

from unirank.core.json_loader import load_database_folder


def test_web_payload_keeps_structured_profiles_and_city_name():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, report = load_database_folder(database, strict=False)

    structured_rows = [
        row for row in dataframe.to_dict(orient="records")
        if isinstance(row.get("source_profile"), dict)
        and isinstance(row.get("cost_profile"), dict)
    ]

    assert report.records_loaded > 0
    assert structured_rows
    assert all(isinstance(row.get("city"), str) for row in structured_rows)
    assert all(isinstance(row.get("program_name"), str) and row["program_name"].strip() for row in structured_rows)
    assert all("language_profile" in row for row in structured_rows)


def test_web_payload_suppresses_institution_only_research_candidates():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, report = load_database_folder(database, strict=False)

    assert "tomsk-polytechnic-tpu" not in set(dataframe["id"])
    assert any(
        issue.record_id == "tomsk-polytechnic-tpu"
        and "without a verified programme name" in issue.message
        for issue in report.issues
    )


def test_v2_records_preserve_source_currency_without_fake_eur_conversion():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    norway = dataframe.loc[dataframe["id"] == "no-uit-aerospace-engineering-msc"].iloc[0]
    lithuania = dataframe.loc[dataframe["id"] == "lt-vilnius-tech-aerospace-msc"].iloc[0]
    estonia = dataframe.loc[dataframe["id"] == "ee-ut-robotics-computer-engineering-space-msc"].iloc[0]
    ireland = dataframe.loc[dataframe["id"] == "ie-ucd-space-science-technology-msc"].iloc[0]
    assert pd.isna(norway["tuition_eur_per_year"])
    assert norway["cost_profile"]["tuition_items"][0]["currency"] == "NOK"
    assert lithuania["tuition_eur_per_year"] == 6450
    assert lithuania["deadline_winter_closes"] == ""
    assert estonia["tuition_eur_per_year"] == 7200
    assert estonia["deadline_winter_closes"] == ""
    assert ireland["tuition_eur_per_year"] == 29500
    assert ireland["deadline_winter_closes"] == ""


def test_specialized_non_eu_scope_reaches_public_tuition_field():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    craiova = dataframe.loc[
        dataframe["id"] == "ro-university-craiova-complex-systems-aerospace-engineering-msc"
    ].iloc[0]
    assert craiova["tuition_eur_per_year"] == 3500
    assert craiova["cost_profile"]["tuition_items"][1]["mandatory"] is False


def test_unknown_non_eu_eligibility_stays_visible_without_invented_cost():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    mta = dataframe.loc[
        dataframe["id"] == "ro-military-technical-academy-aerospace-systems-engineering-msc"
    ].iloc[0]
    assert mta["eligibility_profile"]["eligible_for_non_eu"] is None
    assert pd.isna(mta["tuition_eur_per_year"])
    assert mta["teaching_language"] == ["Romanian"]
    assert bool(mta["needs_verification"]) is True


def test_tuhh_foreign_degree_route_reaches_public_payload_with_conditions():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    tuhh = dataframe.loc[dataframe["id"] == "de_tuhh_aeronautics_msc"].iloc[0]
    assert tuhh["eligibility_profile"]["eligible_for_non_eu"] is True
    assert tuhh["admission_mode"] == "direct_online_application_to_tuhh_with_foreign_degree_assessment"
    assert "proof_of_required_german_language_proficiency" in tuhh["eligibility_profile"]["required_documents"]
    assert tuhh["data_quality"]["status"] == "partial"
    assert bool(tuhh["needs_verification"]) is True


def test_stanford_language_policy_preserves_current_test_scale_and_gre_rule():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    stanford = dataframe.loc[dataframe["id"] == "stanford-aa"].iloc[0]
    assert stanford["teaching_language"] == ["English"]
    assert stanford["language_profile"]["minimum_scores"]["toefl_before_2026_01_21"] == 90
    assert stanford["language_profile"]["minimum_scores"]["toefl_on_or_after_2026_01_21"] == 4.5
    assert stanford["language_profile"]["minimum_scores"]["ielts_academic"] == 7
    assert stanford["eligibility_profile"]["gre"]["policy"] == "not_required_and_not_considered"
    assert stanford["data_quality"]["status"] == "partial"


def test_caltech_international_route_keeps_conflicting_english_rules_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    caltech = dataframe.loc[dataframe["id"] == "caltech-galcit"].iloc[0]
    assert caltech["teaching_language"] == ["English"]
    assert caltech["eligibility_profile"]["eligible_for_non_eu"] is True
    assert caltech["eligibility_profile"]["gre"]["policy"] == "optional"
    assert caltech["language_profile"]["minimum_scores"] == {}
    assert "programme-specific TOEFL rule" in caltech["language_profile"]["policy_conflict"]["en"]
    assert caltech["data_quality"]["status"] == "partial"


def test_caltech_space_ms_has_current_cost_housing_curriculum_and_funding_scope():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    caltech = dataframe.loc[dataframe["id"] == "caltech-galcit"].iloc[0]
    cost = caltech["cost_profile"]
    raw_records = json.loads((database / "amerika.json").read_text(encoding="utf-8"))
    raw_caltech = next(item for item in raw_records if item.get("id") == "caltech-galcit")
    assert raw_caltech["university_aliases"] == ["Caltech", "CIT"]
    curriculum = caltech["curriculum_profile"]
    funding = caltech["scholarship_profile"]
    housing = caltech["living_profile"]
    timeline = caltech["application_timeline_profile"]
    research = caltech["research_profile"]

    assert caltech["duration_years"] == 1
    assert caltech["qs_ranking"] == 7
    assert cost["academic_year"] == "2026/2027"
    assert cost["total_tuition_and_mandatory_fees_usd_per_year"] == 71022
    assert cost["health_insurance_premium_usd"] is None
    assert cost["total_cost_of_attendance_usd_per_year"] is None
    assert funding["automatic_consideration"] is True
    assert funding["separate_application_required"] is False
    assert funding["terminal_ms_often_self_supported"] is True
    assert funding["phd_stipend_not_applicable"] is True
    assert housing["housing_guaranteed"] is True
    assert housing["latest_published_housing_deadline"] == "2026-04-30"
    assert housing["official_rent_items"][0]["amount_usd_min"] == 830
    assert curriculum["official_total_units"] == 135
    assert curriculum["listed_requirement_component_sum_units"] == 138
    assert curriculum["official_arithmetic_discrepancy"] is True
    assert curriculum["thesis_required"] is False
    assert curriculum["research_required"] is False
    assert timeline["next_dated_deadline"] is None
    assert timeline["financial_proof_required_before_i20_or_ds2019"] is None
    assert research["jpl_collaboration_opportunities"] is True
    assert research["jpl_access_guaranteed"] is False
    assert caltech["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert len(caltech["source_profile"]["source_log"]) == 32


def test_uc_berkeley_me_meng_scopes_professional_degree_cost_funding_and_housing():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    berkeley = dataframe.loc[dataframe["id"] == "uc-berkeley-me"].iloc[0]
    eligibility = berkeley["eligibility_profile"]
    language = berkeley["language_profile"]
    curriculum = berkeley["curriculum_profile"]
    cost = berkeley["cost_profile"]
    funding = berkeley["scholarship_profile"]
    housing = berkeley["living_profile"]
    timeline = berkeley["application_timeline_profile"]

    assert berkeley["program_degree"] == "MEng"
    assert berkeley["qs_ranking"] == 20
    assert eligibility["eligible_for_international_applicants"] is True
    assert eligibility["application_fee_usd_international"] == 155
    assert eligibility["gre"]["policy"] == "not_required"
    assert language["teaching_language"] == ["Unknown"]
    assert language["fall_2027_score_deadline"] == "2026-12-01T20:59:00-08:00"

    assert curriculum["total_units"] == 25
    assert sum(item["units"] for item in curriculum["requirement_components"]) == 25
    assert curriculum["aerospace_concentration_minimum_listed_courses"] == 2
    assert curriculum["comprehensive_exam_required"] is True
    assert curriculum["thesis_required"] is False
    assert curriculum["research_required"] is False

    assert cost["academic_year"] == "2025/2026"
    assert cost["current_for_fall_2027"] is False
    assert cost["total_tuition_and_required_fees_usd_nonresident"] == 71435.50
    assert cost["derived_same_year_total_budget_usd"] == 108209.50
    assert cost["complete_program_cost_usd_fall_2027"] is None

    assert funding["application_mode"] == "mixed"
    assert funding["automatic_consideration"] is False
    assert funding["automatic_consideration_for_some_awards"] is True
    assert funding["opportunities"][0]["international_eligible"] is True
    assert funding["opportunities"][1]["admission_application_grant_section_required"] is True

    assert housing["housing_guaranteed"] is False
    assert housing["housing_application_continuously_open"] is True
    assert housing["graduate_housing_rate_usd_per_person_month_min"] == 1530
    assert housing["graduate_housing_rate_usd_per_person_month_max"] == 2495
    assert timeline["application_deadline"] == "2027-01-06T20:59:00-08:00"
    assert timeline["english_score_deadline_if_required"] == "2026-12-01T20:59:00-08:00"
    assert berkeley["research_profile"]["individual_lab_place_guaranteed"] is False
    assert berkeley["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert len(berkeley["source_profile"]["source_log"]) == 37
    assert berkeley["data_quality"]["status"] == "partial"


def test_cambridge_engineering_preserves_official_overseas_gbp_commitment():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    cambridge = dataframe.loc[dataframe["id"] == "university-of-cambridge"].iloc[0]
    cost = cambridge["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_gbp_per_year"] == 41304
    assert cost["living_cost_gbp_per_year"] == 19860
    assert cost["total_academic_and_living_cost_gbp_per_year"] == 61164
    assert pd.isna(cambridge["tuition_eur_per_year"])


def test_oxford_research_msc_keeps_closed_cycle_and_no_gre_claim_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    oxford = dataframe.loc[dataframe["id"] == "university-of-oxford"].iloc[0]
    assert oxford["eligibility_profile"]["eligible_for_non_eu"] is True
    assert oxford["eligibility_profile"]["gre"]["policy"] == "not_sought"
    assert oxford["language_profile"]["minimum_scores"]["ielts_academic"]["overall"] == 7.5
    assert oxford["cost_profile"]["tuition_gbp_per_year"] == 34700
    assert oxford["scholarship_profile"]["application_mode"] == "mixed"
    deadline = oxford["application_timeline_profile"]["deadline_events"][0]
    assert deadline["status"] == "closed"
    assert deadline["date"] is None


def test_glasgow_aerospace_keeps_language_transition_and_scoped_living_budget():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    glasgow = dataframe.loc[dataframe["id"] == "university-of-glasgow"].iloc[0]
    language = glasgow["language_profile"]
    assert glasgow["teaching_language"] == ["English"]
    assert language["minimum_scores"]["ielts_academic"]["overall"] == 6.5
    assert language["minimum_scores"]["toefl_ibt_from_2026_01_21"]["overall"] == 92
    assert glasgow["application_timeline_profile"]["non_eu_deadline"] == "2026-08-24"
    rent = glasgow["living_profile"]["official_rent_items"][0]
    assert rent["amount_min"] == 141.47
    assert rent["amount_max"] == 258.72
    budget = glasgow["living_profile"]["official_living_cost_items"][0]
    assert budget["amount"] == 31958
    assert budget["applicant_scope"] == "new_US_federal_student_aid_borrower"


def test_southampton_space_keeps_conditional_deadlines_housing_and_funding_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    southampton = dataframe.loc[
        dataframe["id"] == "university-of-southampton"
    ].iloc[0]
    assert southampton["teaching_language"] == ["English"]
    assert southampton["language_profile"]["minimum_scores"]["ielts_academic"]["overall"] == 6.5
    assert southampton["eligibility_profile"]["gre"]["policy"] == "not_listed_in_checked_official_required_documents"
    assert southampton["eligibility_profile"]["references_required"] is False
    assert southampton["cost_profile"]["tuition_gbp_full_programme"] == 35000
    assert southampton["cost_profile"]["application_assessment_fee_gbp"] == 0
    assert southampton["curriculum_profile"]["mandatory_course_count"] == 7
    assert southampton["curriculum_profile"]["published_elective_option_count"] == 5
    assert southampton["application_timeline_profile"]["non_eu_deadline"] == "2026-07-21"
    assert southampton["application_timeline_profile"]["international_latest_deadline_if_atas_not_required"] == "2026-08-19"
    housing = southampton["living_profile"]["housing_guarantee"]
    assert housing["available"] is True
    assert housing["application_deadline"] == "2026-08-01"
    scholarship = southampton["scholarship_profile"]["opportunities"][0]
    assert scholarship["application_mode"] == "automatic"
    assert scholarship["status"] == "awarded_closed"
    assert scholarship["award"]["amount"] == 3000


def test_bristol_aerospace_keeps_closed_routes_and_survey_cost_scope_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    bristol = dataframe.loc[dataframe["id"] == "university-of-bristol"].iloc[0]
    assert bristol["teaching_language"] == ["English"]
    language = bristol["language_profile"]
    assert language["minimum_scores"]["ielts_academic"]["overall"] == 6.5
    assert language["minimum_scores"]["toefl_ibt_from_2026_01_21"]["overall"] == 4.5
    assert bristol["cost_profile"]["tuition_gbp_full_programme"] == 34900
    assert bristol["eligibility_profile"]["gre"]["policy"] == "not_listed_in_checked_official_required_documents"
    assert bristol["curriculum_profile"]["planned_unit_selection_count"] == 6
    assert bristol["application_timeline_profile"]["non_eu_deadline"] == "2026-08-13"
    assert bristol["scholarship_profile"]["application_mode"] == "separate"
    assert bristol["scholarship_profile"]["current_cycle_status"] == "closed"
    assert bristol["living_profile"]["housing_guarantee"]["status_as_of_last_checked"] == "deadline_passed"
    assert bristol["living_profile"]["monthly_living_cost_gbp_per_month_estimated"] == 1862


def test_leeds_aerospace_keeps_mixed_funding_deadlines_and_module_scope_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    leeds = dataframe.loc[dataframe["id"] == "university-of-leeds"].iloc[0]
    assert leeds["teaching_language"] == ["English"]
    assert leeds["language_profile"]["minimum_scores"]["ielts_academic"]["overall"] == 6.5
    assert leeds["eligibility_profile"]["gre"]["policy"] == "not_listed_in_checked_official_required_documents"
    assert leeds["cost_profile"]["tuition_gbp_full_programme"] == 33500
    assert leeds["cost_profile"]["student_visa_tuition_deposit_gbp"] == 2000
    assert leeds["curriculum_profile"]["mandatory_course_count"] == 4
    assert leeds["curriculum_profile"]["published_elective_option_count"] == 12
    assert leeds["curriculum_profile"]["exact_elective_selection_count"] is None
    assert leeds["application_timeline_profile"]["non_eu_deadline"] == "2026-07-31"
    regional = leeds["scholarship_profile"]["opportunities"][0]
    excellence = leeds["scholarship_profile"]["opportunities"][1]
    assert regional["application_mode"] == "automatic"
    assert regional["turkey_passport_eligible"] is True
    assert regional["award"]["amount"] == 6000
    assert excellence["status"] == "closed"
    assert excellence["application_deadline"] == "2026-05-29"
    assert leeds["living_profile"]["housing_guarantee"]["status_as_of_last_checked"] == "deadline_passed"
    assert leeds["living_profile"]["living_cost_gbp_per_week_min"] == 199
    assert leeds["living_profile"]["living_cost_gbp_per_week_max"] == 423


def test_sheffield_aerospace_keeps_routes_accreditation_and_deadline_states_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    sheffield = dataframe.loc[dataframe["id"] == "university-of-sheffield"].iloc[0]
    assert sheffield["teaching_language"] == ["English"]
    language = sheffield["language_profile"]
    assert language["minimum_scores"]["ielts_academic"]["overall"] == 6.5
    assert language["minimum_scores"]["toefl_ibt_from_january_2026"]["overall"] == 4.5
    assert sheffield["eligibility_profile"]["references_required"] is False
    assert sheffield["eligibility_profile"]["supporting_statement_required"] is False
    assert sheffield["eligibility_profile"]["gre"]["policy"] == "not_listed_in_checked_official_required_documents"
    assert sheffield["cost_profile"]["tuition_gbp_full_programme"] == 32905
    assert sheffield["cost_profile"]["student_visa_tuition_deposit_gbp"] == 2000
    curriculum = sheffield["curriculum_profile"]
    assert len(curriculum["tracks"]) == 2
    assert curriculum["elective_selection_count"] == 4
    assert curriculum["published_elective_option_count"] == 18
    assert curriculum["published_route_credit_total"] == 180
    assert curriculum["accreditation_status"] == "not_currently_accredited"
    scholarship = sheffield["scholarship_profile"]["opportunities"][0]
    assert scholarship["application_mode"] == "automatic_after_eligible_offer_acceptance"
    assert scholarship["status"] == "closed"
    assert scholarship["award"]["amount"] == 3000
    assert sheffield["application_timeline_profile"]["non_eu_deadline"] == "2026-09-01"
    housing = sheffield["living_profile"]["housing_guarantee"]
    assert housing["offer_acceptance_deadline"] == "2026-07-26"
    assert housing["application_deadline"] == "2026-09-03"


def test_liverpool_aerospace_keeps_credit_gap_turkish_funding_and_housing_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    liverpool = dataframe.loc[
        dataframe["id"] == "university-of-liverpool"
    ].iloc[0]
    assert liverpool["teaching_language"] == ["English"]
    language = liverpool["language_profile"]
    assert language["minimum_scores"]["ielts_academic"]["overall"] == 6.5
    assert language["minimum_scores"]["toefl_ibt_from_2026_01_21"]["overall"] == 4.5
    eligibility = liverpool["eligibility_profile"]
    assert eligibility["gre"]["policy"] == "not_listed_in_checked_official_required_documents"
    assert eligibility["references_required"] is False
    assert liverpool["cost_profile"]["tuition_gbp_full_programme"] == 34000
    assert liverpool["cost_profile"]["student_visa_tuition_deposit_gbp"] == 2000
    curriculum = liverpool["curriculum_profile"]
    assert curriculum["mandatory_course_count_including_conditional_writing_and_project"] == 8
    assert curriculum["published_elective_option_count"] == 7
    assert curriculum["exact_elective_selection_count"] is None
    assert curriculum["published_module_credit_sum_in_each_stated_route"] == 172.5
    assert curriculum["credit_reconciliation_status"] == "needs_verification"
    excellence, advancement = liverpool["scholarship_profile"]["opportunities"]
    assert excellence["application_mode"] == "automatic"
    assert excellence["award"]["amount"] == 7000
    assert advancement["turkey_nationality_eligible"] is True
    assert advancement["award"]["amount"] == 5000
    timeline = liverpool["application_timeline_profile"]
    assert timeline["non_eu_deadline"] == "2026-07-17"
    assert timeline["deadline_events"][0]["status"] == "closed"
    living = liverpool["living_profile"]
    assert living["housing_guarantee"]["status_as_of_last_checked"] == "deadline_passed"
    assert living["housing_rent_gbp_per_week_min"] == 115
    assert living["housing_rent_gbp_per_week_max"] == 271.53
    assert len(living["official_rent_items"]) == 12


def test_edinburgh_no_program_candidate_stays_out_of_programme_catalogue():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)

    assert "university-of-edinburgh" not in set(dataframe["id"].dropna())
    queue = json.loads(
        (root / "research_queue" / "program_candidates_v2.json").read_text(
            encoding="utf-8"
        )
    )
    exclusion = next(
        item
        for item in queue["candidates"]
        if item.get("candidate_id")
        == "uk-edinburgh-no-dedicated-aerospace-space-masters"
    )
    assert exclusion["discovery_status"] == "excluded_no_eligible_program"
    assert exclusion["program_name"] is None
    assert len(exclusion["catalogue_programmes_checked"]) == 11
    assert len(exclusion["discovery_sources"]) == 3


def test_birmingham_space_keeps_deposit_conflict_turkish_funding_and_housing_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    birmingham = dataframe.loc[
        dataframe["id"] == "university-of-birmingham"
    ].iloc[0]
    assert birmingham["teaching_language"] == ["English"]
    language = birmingham["language_profile"]
    assert language["minimum_scores"]["ielts"]["overall"] == 6.5
    assert language["minimum_scores"]["toefl_ibt_from_2026_01"]["overall"] == 4.5
    assert birmingham["eligibility_profile"]["gre"]["policy"] == "not_listed_in_checked_official_course_or_application_requirements"
    cost = birmingham["cost_profile"]
    assert cost["tuition_gbp_full_programme"] == 33660
    assert cost["student_visa_tuition_deposit_gbp"] is None
    assert cost["deposit_public_page_conflict"]["amounts_published_gbp"] == [2000, 3000]
    curriculum = birmingham["curriculum_profile"]
    assert curriculum["mandatory_course_count"] == 5
    assert curriculum["selected_elective_course_count"] == 3
    assert curriculum["total_modules_taken_including_research_project"] == 8
    assert curriculum["total_uk_credits"] == 180
    high_fliers, esa = birmingham["scholarship_profile"]["opportunities"]
    assert high_fliers["application_mode"] == "automatic"
    assert high_fliers["turkey_domicile_eligible"] is True
    assert high_fliers["award"]["amount"] == 5000
    assert esa["turkey_nationality_eligible_on_published_list"] is False
    assert birmingham["application_timeline_profile"]["non_eu_deadline"] == "2026-07-17"
    living = birmingham["living_profile"]
    assert living["housing_guarantee"]["deadline_status"] == "passed"
    assert living["housing_budget_gbp_per_year_min"] == 5335
    assert living["housing_budget_gbp_per_year_max"] == 17966
    assert len(living["official_rent_items"]) == 17


def test_nottingham_mechanical_keeps_aerospace_stream_and_weak_space_fit_explicit():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    nottingham = dataframe.loc[
        dataframe["id"] == "university-of-nottingham"
    ].iloc[0]
    assert nottingham["program_name"] == "Mechanical Engineering MSc"
    assert nottingham["teaching_language"] == ["English"]
    assert nottingham["language_profile"]["minimum_scores"]["ielts"]["overall"] == 6.0
    assert nottingham["eligibility_profile"]["turkey_degree_guidance"]["typical_2_1_equivalent_gpa_out_of_4"] == 3.0
    assert nottingham["eligibility_profile"]["gre"]["policy"] == "not_listed_in_checked_official_course_or_application_requirements"
    assert nottingham["cost_profile"]["tuition_gbp_full_programme"] == 33000
    assert nottingham["cost_profile"]["student_visa_cas_deposit_gbp"] == 4500
    curriculum = nottingham["curriculum_profile"]
    assert curriculum["selected_track"] == "Aerospace"
    assert curriculum["total_uk_credits"] == 180
    assert curriculum["mandatory_course_count_including_one_selected_analysis_module"] == 8
    assert curriculum["exact_elective_selection_count"] is None
    assert curriculum["total_modules_taken_min"] == 9
    assert curriculum["total_modules_taken_max"] == 10
    assert curriculum["space_curriculum_depth"] == "introductory_only_within_fundamentals_module"
    assert nottingham["category_profile"]["category_scores"]["space_engineering"] == 20
    scholarship = nottingham["scholarship_profile"]["opportunities"][0]
    assert scholarship["application_mode"] == "automatic_on_enrolment"
    assert scholarship["turkey_eligible"] is True
    assert scholarship["award"]["amount"] == 3000
    assert nottingham["living_profile"]["housing_guarantee"]["available"] is True
    assert nottingham["living_profile"]["monthly_living_cost_gbp_per_month_min"] == 800
    assert nottingham["application_timeline_profile"]["deadline_events"][0]["date"] is None


def test_tudelft_scholarship_keeps_separate_closed_cycle_and_blocked_source_explicit():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    delft = dataframe.loc[
        dataframe["id"] == "netherlands_delft_msc_aerospace"
    ].iloc[0]
    gre = delft["eligibility_profile"]["gre"]
    assert gre["policy"] == "required_for_international_bsc_applicants_to_aerospace_engineering_in_the_2026_27_cycle"
    assert gre["minimum_scores"] == {
        "verbal_reasoning": 154,
        "quantitative_reasoning": 163,
        "analytical_writing": 4.0,
    }
    scholarship = delft["scholarship_profile"]
    assert scholarship["application_mode"] == "separate"
    assert scholarship["automatic_consideration"] is False
    assert scholarship["separate_application_required"] is True
    # An accessible official scholarship page now backs the record, so the
    # integrity gate surfaces the opportunity instead of stripping it.  The
    # award itself is still labelled as a closed cycle, and the dedicated page
    # that blocks automated access is still recorded as blocked below.
    assert len(scholarship["opportunities"]) == 1

    raw_payload = json.loads(
        (database / "hollanda.json").read_text(encoding="utf-8")
    )
    raw_delft = next(
        row
        for row in raw_payload["programs"]
        if row["id"] == "netherlands_delft_msc_aerospace"
    )
    raw_scholarship = raw_delft["scholarship_profile"]
    opportunity = raw_scholarship["opportunities"][0]
    assert opportunity["status"] == "closed_awards_made"
    assert opportunity["turkey_nationality_eligible"] is True
    assert opportunity["deadline"] == "2025-12-01T23:59:00+01:00"
    assert opportunity["award"]["living_expense_amount"] is None
    sources = raw_delft["source_profile"]["source_log"]
    official = next(
        source
        for source in sources
        if source["url"] == raw_scholarship["scholarship_application_url"]
    )
    assert official["access_status"] == "blocked"
    assert raw_delft["source_profile"]["field_confidence"]["scholarship"] == "medium"
    # The blocked page is not the only scholarship evidence any more: an
    # accessible official scholarship page sits beside it.
    assert any(
        source["source_type"] == "official_scholarship_page" and source["access_status"] == "ok"
        for source in sources
    )
    # Every playbook step derived from the blocked page carries an explicit
    # instruction to re-confirm it in a browser.
    playbook = raw_scholarship["playbook"][0]
    assert playbook["needs_human_verification"] is True
    assert playbook["verification_note"]["en"]


def test_tue_mechanical_stays_adjacent_and_does_not_invent_non_eu_cost_or_admission():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    tue = dataframe.loc[
        dataframe["id"] == "netherlands_tue_msc_mechanical_systems_control"
    ].iloc[0]
    assert tue["teaching_language"] == ["English"]
    assert tue["language_profile"]["minimum_scores"]["ielts_academic"]["overall"] == 6.5
    assert tue["application_timeline_profile"]["non_eu_deadline"] == "2027-05-01"
    assert tue["living_profile"]["official_rent_items"][0]["monthly_total_eur"] == 606.33
    assert tue["curriculum_profile"]["research_clusters"] == [
        "Dynamical Systems Design",
        "Computational and Experimental Mechanics",
        "Thermo Fluids Engineering",
    ]
    assert tue["curriculum_profile"]["exact_course_count"] is None

    raw_payload = json.loads(
        (database / "hollanda.json").read_text(encoding="utf-8")
    )
    raw_tue = next(
        row
        for row in raw_payload["programs"]
        if row["id"] == "netherlands_tue_msc_mechanical_systems_control"
    )
    assert raw_tue["programme_fit_class"] == "adjacent_mechanical_degree_with_aerospace_applications_not_aerospace_or_space_degree"
    assert raw_tue["cost_profile"]["tuition_eur_per_year_estimated"] is None
    assert raw_tue["cost_profile"]["historical_non_eu_master_tuition_reference"]["use_for_2026_27"] is False
    assert raw_tue["eligibility_profile"]["required_previous_degree"] is None
    assert raw_tue["scholarship_profile"]["application_mode"] == "unknown"
    assert set(raw_tue["data_quality"]["unverified_critical_fields"]) == {
        "admission",
    }


def test_polito_foreign_degree_cycle_distinguishes_application_visa_and_enrolment_dates():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    polito = dataframe.loc[dataframe["id"] == "polito-msc-aerospace"].iloc[0]
    assert polito["eligibility_profile"]["eligible_for_non_eu"] is True
    assert polito["eligibility_profile"]["cv_required"] is True
    assert polito["eligibility_profile"]["gre"]["policy"] == "optional_supporting_document_not_programme_requirement"
    assert polito["language_profile"]["italian_level_required"] == "B2"
    assert polito["language_profile"]["minimum_scores"]["ielts_academic"]["overall"] == 5.5
    timeline = polito["application_timeline_profile"]
    assert timeline["non_eu_deadline"] == "2026-04-20T14:00:00+02:00"
    assert timeline["visa_sensitive_deadline"].startswith("2026-07-15")
    assert timeline["enrollment_deadline"].startswith("2026-10-05")
    assert polito["data_quality"]["unverified_critical_fields"] == []


def test_sapienza_non_eu_route_keeps_all_three_deadlines_and_turkish_language_warning():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    sapienza = dataframe.loc[
        dataframe["id"] == "sapienza_space_astronautical_msc"
    ].iloc[0]
    assert sapienza["eligibility_profile"]["eligible_for_non_eu"] is True
    assert sapienza["eligibility_profile"]["minimum_gpa"] == 75
    assert sapienza["eligibility_profile"]["interview_required"] is True
    assert sapienza["eligibility_profile"]["gre"]["policy"] == "not_listed_as_required_or_recommended_for_this_programme"
    language = sapienza["language_profile"]
    assert language["minimum_scores"]["ielts_academic"]["overall"] == 5.5
    assert language["minimum_scores"]["toefl_ibt"]["overall"] == 80
    assert "Turkey" in language["verification_notes"]["en"]
    timeline = sapienza["application_timeline_profile"]
    assert timeline["non_eu_deadline"] == "2026-05-15"
    assert timeline["visa_sensitive_deadline"] == "2026-06-30T23:59:00+02:00"
    assert timeline["enrollment_deadline"].startswith("2026-09-15")
    assert {event["event"] for event in timeline["deadline_events"]} >= {
        "movein_non_eu_visa_deadline",
        "universitaly_deadline",
        "infostud_non_eu_visa_deadline",
    }
    assert sapienza["data_quality"]["unverified_critical_fields"] == []


def test_unina_distinguishes_zero_contribution_mandatory_fees_and_separate_adisurc_application():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    unina = dataframe.loc[dataframe["id"] == "unina_aerospace_master"].iloc[0]
    assert unina["eligibility_profile"]["eligible_for_non_eu"] is True
    assert unina["eligibility_profile"]["gre"]["policy"] == "not_listed_as_required_in_checked_official_sources"
    language = unina["language_profile"]
    assert language["primary_teaching_language"] == "Italian"
    assert language["italian_required"] is True
    assert language["english_required_at_entry"] is False

    cost = unina["cost_profile"]
    assert cost["student_contribution_eur"] == 0
    assert cost["mandatory_fees_eur_per_year_min"] == 167
    assert cost["mandatory_fees_eur_per_year_max"] == 189
    assert cost["total_academic_cost_eur_per_year_estimated"] is None

    scholarship = unina["scholarship_profile"]
    assert scholarship["application_mode"] == "separate"
    assert scholarship["automatic_consideration"] is False
    assert scholarship["scholarship_deadline"] == "2026-09-10T12:00:00+02:00"
    assert scholarship["opportunities"][0]["amount_eur"] == 7171.11

    living = unina["living_profile"]
    assert living["housing_access"] == "not_guaranteed"
    assert living["average_room_rent_eur_min"] == 250
    assert living["average_room_rent_eur_max"] == 500
    assert len(living["official_rent_items"]) == 3

    timeline = unina["application_timeline_profile"]
    assert timeline["non_eu_deadline"] == "2026-06-15"
    assert timeline["visa_sensitive_deadline"] == "2026-11-30"
    events = {event["event"]: event for event in timeline["deadline_events"]}
    assert events["universitaly_pre_enrolment_deadline_overseas_non_eu"]["status"] == "closed"
    assert events["adisurc_scholarship_and_services_deadline"]["status"] == "open_as_of_last_checked"
    assert unina["data_quality"]["unverified_critical_fields"] == []


def test_poliba_uses_current_two_campuses_and_does_not_turn_first_payment_into_full_tuition():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    # PoliBa is a teaching-partner view of the same joint degree whose
    # administrative/application seat is UniSalento.  Keep its research data,
    # but never present it as a second independent student choice.
    assert "poliba_aerospace_master" not in set(dataframe["id"])
    raw_payload = json.loads((database / "italy.json").read_text(encoding="utf-8"))
    poliba = next(
        row for row in raw_payload["universities"]
        if row["id"] == "poliba_aerospace_master"
    )
    assert poliba["joint_program_id"] == "it-unisalento-poliba-aerospace-engineering-msc"
    assert poliba["catalogue_relationship"]["canonical_record_id"] == "universita-del-salento"
    assert poliba["catalogue_relationship"]["rankable_as_independent_choice"] is False
    assert poliba["city"] == "Taranto / Lecce"
    assert poliba["teaching_language"] == ["English"]
    assert poliba["curriculum_profile"]["tracks"] == ["Aerospace Design", "Aeronautics Design"]
    assert poliba["curriculum_profile"]["exact_course_count"] is None
    assert poliba["eligibility_profile"]["eligible_for_non_eu"] is True
    assert poliba["eligibility_profile"]["gre"]["policy"] == "not_listed_as_required_in_checked_official_sources"

    cost = poliba["cost_profile"]
    assert cost["mandatory_first_installment_eur"] == 136
    assert cost["tuition_eur_per_year_estimated"] is None
    assert cost["historical_full_contribution_reference"]["use_for_2026_27"] is False

    scholarship = poliba["scholarship_profile"]
    assert scholarship["application_mode"] == "separate"
    assert scholarship["scholarship_deadline"] == "2026-08-13T12:00:00+02:00"
    assert scholarship["opportunities"][0]["amount_eur"] == 7172

    timeline = poliba["application_timeline_profile"]
    events = {event["event"]: event for event in timeline["deadline_events"]}
    assert events["first_esse3_master_admission_window"]["status"] == "open_as_of_last_checked"
    assert events["adisu_benefits_deadline"]["status"] == "closed"
    assert timeline["non_eu_deadline"] is None

    assert poliba["living_profile"]["housing_access"] == "not_guaranteed"
    assert poliba["data_quality"]["unverified_critical_fields"] == []
    assert poliba["data_quality"]["status"] == "partial"


def test_unisalento_is_the_verified_canonical_joint_aerospace_application_route():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, report = load_database_folder(database, strict=False)

    unisalento = dataframe.loc[dataframe["id"] == "universita-del-salento"].iloc[0]
    assert unisalento["city"] == "Brindisi"
    assert unisalento["teaching_language"] == ["English"]
    assert unisalento["ects"] == 120
    assert unisalento["joint_program_id"] == "it-unisalento-poliba-aerospace-engineering-msc"
    relationship = unisalento["catalogue_relationship"]
    assert relationship["role"] == "canonical_administrative_and_application_record"
    assert relationship["rankable_as_independent_choice"] is True

    eligibility = unisalento["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["non_eu_quota"] == 30
    assert eligibility["minimum_gpa"]["percentage"] == 70
    assert eligibility["interview_required"] is True
    assert eligibility["application_fee_eur"] == 23
    assert eligibility["gre"]["policy"] == "not_listed_as_required_or_scored_in_checked_2026_27_programme_sources"

    language = unisalento["language_profile"]
    assert language["english_level_required"] == "B2 CEFR"
    assert language["medium_of_instruction_accepted"] is True
    assert language["english_interview_assessment_required"] is True

    cost = unisalento["cost_profile"]
    assert cost["tuition_eur_per_year_estimated"] == 1000
    assert cost["non_eu_flat_fee"] == 1000
    assert cost["regional_tax_eur"] is None
    assert cost["regional_tax_eur_approx"] == 190

    scholarship = unisalento["scholarship_profile"]
    assert scholarship["application_mode"] == "separate"
    assert scholarship["automatic_consideration"] is False
    opportunities = {item["name"]: item for item in scholarship["opportunities"]}
    assert opportunities["ADISU Puglia Benefits and Services 2026/27"]["status_as_of_last_checked"] == "closed"
    assert opportunities["ISUFI second-level student admission 2026/27"]["status_as_of_last_checked"] == "open"
    assert opportunities["ISUFI second-level student admission 2026/27"]["places_technical_scientific"] == 2

    assert unisalento["living_profile"]["housing_access"] == "not_guaranteed"
    assert unisalento["living_profile"]["average_room_rent_eur"] is None
    assert unisalento["curriculum_profile"]["exact_course_count"] is None
    assert unisalento["curriculum_profile"]["historical_curriculum_snapshot"]["use_as_current_guarantee"] is False
    assert unisalento["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert unisalento["student_sentiment_profile"]["student_sentiment_sources"] == []
    assert unisalento["data_quality"]["status"] == "verified"
    assert unisalento["data_quality"]["unverified_critical_fields"] == []
    assert any(
        issue.record_id == "poliba_aerospace_master"
        and "non-independent joint-programme" in issue.message
        for issue in report.issues
    )


def test_unipa_separates_italian_teaching_english_entry_skill_flat_fee_and_ersu_services():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    unipa = dataframe.loc[dataframe["id"] == "unipa_aerospace_master"].iloc[0]
    assert unipa["teaching_language"] == ["Italian"]
    language = unipa["language_profile"]
    assert language["italian_level_required"].startswith("B2 CEFR")
    assert language["english_required_at_entry"] is True
    assert language["english_level_required"].startswith("B2 CEFR")
    assert language["minimum_scores"] == {}

    eligibility = unipa["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["required_ects"]["total_subject_specific_cfu"] == 63
    assert eligibility["gre"]["policy"] == "not_listed_as_required_in_checked_official_sources"

    cost = unipa["cost_profile"]
    assert cost["tuition_eur_per_year_estimated"] == 356
    assert cost["non_eu_flat_fee"] == 356
    assert cost["tuition_items"][1]["amount_eur"] is None

    scholarship = unipa["scholarship_profile"]
    assert scholarship["application_mode"] == "separate"
    assert scholarship["scholarship_deadline"] == "2026-07-22T14:00:00+02:00"
    assert scholarship["opportunities"][0]["amount_eur"] == 7171.11

    living = unipa["living_profile"]
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_options"][0]["palermo_beds_total"] == 913
    assert living["official_rent_items"][0]["monthly_rent_eur"] == 0
    assert living["average_room_rent_eur"] is None

    curriculum = unipa["curriculum_profile"]
    assert curriculum["current_live_course_count"]["first_year_2026_27_mandatory_taught_courses"] == 6
    assert curriculum["exact_course_count"] is None
    assert curriculum["thesis_ects"] == 15

    events = {
        event["event"]: event
        for event in unipa["application_timeline_profile"]["deadline_events"]
    }
    assert events["second_overseas_non_eu_master_call"]["status"] == "closed"
    assert events["ersu_scholarship_and_housing_application"]["status"] == "closed"
    assert unipa["data_quality"]["unverified_critical_fields"] == []
    assert unipa["data_quality"]["status"] == "partial"


def test_unitn_space_track_keeps_new_programme_delivery_risk_and_noneu_mechanics_explicit():
    root = Path(__file__).parents[1]
    database = root / "data_base"
    dataframe, _ = load_database_folder(database, strict=False)

    unitn = dataframe.loc[dataframe["id"] == "unitn_mechatronics_space"].iloc[0]
    assert unitn["program_name"] == "Intelligent Mechatronics Engineering"
    assert unitn["teaching_language"] == ["English"]

    raw_payload = json.loads((database / "italy.json").read_text(encoding="utf-8"))
    raw_unitn = next(
        row
        for row in raw_payload["universities"]
        if row["id"] == "unitn_mechatronics_space"
    )
    assert raw_unitn["relevance_status"] == "medium"
    assert raw_unitn["programme_fit_class"] == "adjacent_mechatronics_degree_with_space_systems_and_instruments_curriculum_not_aerospace_or_space_degree"
    assert raw_unitn["programme_transition"]["first_year_active_in_2026_27"] is True
    assert raw_unitn["programme_transition"]["second_year_curricula_active_in_2026_27"] is False

    eligibility = unitn["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["reserved_non_eu_places"] == 25
    assert eligibility["minimum_gpa"]["italian_equivalent_weighted_average"] == "23/30"
    assert eligibility["gre"]["policy"] == "not_listed_as_required_or_scored_in_checked_2026_27_programme_sources"
    competition = eligibility["published_2026_27_competition_context"]
    assert competition["listed_application_entries"] == 129
    assert competition["initial_admitted"] == 25
    assert competition["scholarships_available"] == 2

    language = unitn["language_profile"]
    assert language["english_level_required"].startswith("B2 CEFR")
    assert language["medium_of_instruction_accepted"] is True
    assert language["minimum_scores"] == {}

    cost = unitn["cost_profile"]
    assert cost["tuition_eur_per_year_min"] == 0
    assert cost["tuition_eur_per_year_max"] == 4500
    assert cost["tuition_eur_per_year_estimated"] is None
    assert cost["maximum_non_eu_system_fee_eur"] == 6000
    assert cost["place_confirmation_fee_included_in_tuition"] is False

    scholarship = unitn["scholarship_profile"]
    assert scholarship["application_mode"] == "automatic"
    assert scholarship["automatic_consideration"] is True
    assert scholarship["separate_application_required"] is False
    assert scholarship["opportunities"][0]["award_count_for_intelligent_mechatronics_2026_27"] == 2
    assert scholarship["opportunities"][0]["award_eur_per_year"]["female_student_in_stem"] == 8500

    living = unitn["living_profile"]
    assert living["housing_access"] == "guaranteed"
    assert living["housing_guarantee"]["scope"] == "first_academic_year_for_admitted_non_eu_degree_students"
    assert living["average_room_rent_eur"] is None
    assert living["historical_provider_rate_reference"]["use_as_current_2026_27_target_rent"] is False
    assert living["official_rent_items"][0]["room_examples"][0]["listed_total_before_semiannual_adjustment_eur_per_month"] == 380
    assert living["official_rent_items"][1]["listed_total_before_adjustment_eur_per_month"] == 600
    assert living["official_rent_items"][2]["target_turkey_resident_route_applicable"] is False

    curriculum = unitn["curriculum_profile"]
    assert curriculum["selected_track"] == "Space Systems and Instruments"
    assert curriculum["space_course_selection_count"] == 4
    assert len(curriculum["space_course_options"]) == 6
    assert curriculum["thesis_ects"] == 18
    assert curriculum["internship_ects"] == 6
    assert curriculum["delivery_status"]["second_year_2026_27"].startswith("inactive")

    timeline = unitn["application_timeline_profile"]
    assert timeline["non_eu_deadline"] == "2026-03-04T12:00:00+01:00"
    assert timeline["ranking_publication_deadline"] == "2026-05-20"
    assert timeline["universitaly_deadline"] == "within two weeks after place confirmation"
    assert timeline["visa_sensitive_deadline"] == "2026-10-31"

    assert unitn["data_quality"]["unverified_critical_fields"] == []
    # The checked 2026/27 call is historical and the next cycle is intentionally
    # not projected. The record is decision-usable but must remain partial until
    # the next non-EU deadline and second-year delivery are published.
    assert unitn["data_quality"]["status"] == "partial"
    assert unitn["source_profile"]["needs_verification"] is True
    assert unitn["source_profile"]["field_confidence"]["deadline"] == "unknown"


def test_ctu_avionics_uses_current_czk_dorm_examples_without_eur_conversion_or_guarantee():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    ctu = dataframe.loc[
        dataframe["id"] == "cz-ctu-aerospace-engineering-avionics-msc"
    ].iloc[0]

    living = ctu["living_profile"]
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_allocation_mode"] == "competitive_separate_reservation"
    assert living["housing_application_separate"] is True
    assert living["housing_booking_system"] == "ISKAM4"
    assert living["average_room_rent_czk_min"] == 4180
    assert living["average_room_rent_czk_max"] == 7435
    assert living["average_room_rent_eur"] is None
    assert len(living["official_rent_items"]) == 8
    start_cost = living["official_living_cost_items"][0]
    assert start_cost["amount_czk_min"] == 7330
    assert start_cost["amount_czk_max"] == 12895

    assert ctu["scholarship_profile"]["automatic_housing_scholarship_czk_per_month_approx"] == 500
    assert ctu["data_quality"]["unverified_critical_fields"] == []
    assert ctu["data_quality"]["status"] == "verified"


def test_but_aerospace_uses_programme_specific_2026_call_jcmm_and_foreign_dorm_rates():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    but = dataframe.loc[dataframe["id"] == "cz-but-aerospace-technology-msc"].iloc[0]

    eligibility = but["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["entrance_exam"]["subjects"] == ["mathematics", "physics", "technical mechanics"]
    assert eligibility["entrance_exam"]["minimum_points"] == 90
    assert eligibility["entrance_exam"]["maximum_points"] == 300
    assert eligibility["gre"]["policy"] == "not_listed_as_required_or_scored_in_checked_2026_27_programme_sources"

    language = but["language_profile"]
    assert language["english_level_required"].startswith("B1 CEFR")
    assert language["medium_of_instruction_accepted"] is True
    assert "IELTS" in language["minimum_scores"]

    assert but["cost_profile"]["tuition_eur_per_year_estimated"] == 3000
    assert but["cost_profile"]["foreign_education_assessment_fee_eur"] == 30

    scholarship = but["scholarship_profile"]
    assert scholarship["application_mode"] == "separate"
    assert scholarship["automatic_consideration"] is False
    assert scholarship["scholarship_deadline"] == "2026-04-30"
    assert scholarship["opportunities"][0]["programme_eligible"] == "Aerospace Technology"
    assert scholarship["opportunities"][0]["amount_eur_per_year_max"] == 1500

    living = but["living_profile"]
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_allocation_mode"] == "available_by_separate_request"
    assert living["daily_dorm_rate_czk_min"] == 148
    assert living["daily_dorm_rate_czk_max"] == 157
    assert living["average_room_rent_eur"] is None

    timeline = but["application_timeline_profile"]
    assert timeline["non_eu_deadline"] == "2026-03-31"
    events = {event["event"]: event for event in timeline["deadline_events"]}
    assert events["written_entrance_exam"]["date"] == "2026-04-28"
    assert events["non_eu_document_submission"]["date"] == "2026-05-15"
    assert but["data_quality"]["unverified_critical_fields"] == []
    assert but["data_quality"]["status"] == "verified"


def test_upm_muse_uses_current_non_eu_fee_spanish_rule_no_housing_and_real_course_count():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    upm = dataframe.loc[dataframe["id"] == "spain_upm_muse_aerospace"].iloc[0]

    eligibility = upm["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["cohort_size_max"] == 20
    assert eligibility["gre"]["policy"] == "not_listed_as_required"
    assert eligibility["interview_policy"] == "optional_at_academic_committee_discretion"
    assert eligibility["test_required"] is False

    language = upm["language_profile"]
    assert language["teaching_language"] == ["Spanish"]
    assert language["spanish_level_required"] == "B2"
    assert language["english_required"] is False

    cost = upm["cost_profile"]
    assert cost["tuition_items"][0]["rate_eur_per_ects"] == 45.02
    assert cost["tuition_items"][1]["rate_eur_per_ects"] == 84.07
    assert cost["tuition_items"][1]["annual_tuition_eur"] == 5044.20
    assert cost["reservation_deposit_eur"] == 150

    scholarship = upm["scholarship_profile"]
    assert scholarship["application_mode"] == "separate"
    assert scholarship["automatic_consideration"] is False
    assert scholarship["scholarship_deadline"] == "2026-10-07"
    assert scholarship["opportunities"][0]["non_eu_eligibility"] == "needs_verification"

    living = upm["living_profile"]
    assert living["student_housing_available"] is False
    assert living["housing_access"] == "not_offered"
    assert living["housing_application_separate"] is True
    assert living["average_room_rent_eur"] is None

    curriculum = upm["curriculum_profile"]
    assert curriculum["course_count_total_including_thesis"] == 23
    assert curriculum["taught_project_and_seminar_component_count"] == 22
    assert curriculum["thesis_ects"] == 18
    assert curriculum["internship_required"] is False
    assert sum(item["ects"] for item in curriculum["mandatory_courses"]) + curriculum["thesis_ects"] == 120

    timeline = upm["application_timeline_profile"]
    assert timeline["non_eu_deadline"] == "2026-07-01"
    assert timeline["application_rounds"][0]["deadline"] == "2026-03-12"
    assert timeline["application_rounds"][-1]["deadline"] == "2026-09-04"

    assert upm["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert upm["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert upm["data_quality"]["unverified_critical_fields"] == []
    assert upm["data_quality"]["status"] == "verified"


def test_uiuc_ae_ms_separates_pathways_current_usd_costs_funding_and_housing():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    uiuc = dataframe.loc[dataframe["id"] == "uiuc-ae"].iloc[0]

    eligibility = uiuc["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["minimum_gpa"] == 3.0
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["gre"]["policy"] == "optional_waived"
    assert eligibility["interview_required"] is False

    language = uiuc["language_profile"]
    assert language["teaching_language"] == ["English"]
    assert language["english_required"] is True
    assert [item["test"] for item in language["accepted_english_tests"]] == ["TOEFL iBT", "IELTS Academic"]
    assert language["duolingo_program_acceptance"] == "needs_verification"

    cost = uiuc["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_year"] == 40444
    assert cost["mandatory_fees_usd_per_year"] == 5936
    assert cost["total_cost_of_attendance_usd_per_year"] == 67182

    scholarship = uiuc["scholarship_profile"]
    assert scholarship["automatic_consideration"] is True
    assert scholarship["separate_application_required"] is False
    assert "Non-thesis MS students receive no AE departmental funding" in scholarship["funding_notes"]["en"]

    living = uiuc["living_profile"]
    assert living["student_housing_available"] is True
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_application_separate"] is True
    assert living["official_rent_items"][0]["amount_usd_min"] == 6906
    assert living["official_rent_items"][2]["amount_usd_max"] == 1030

    curriculum = uiuc["curriculum_profile"]
    assert curriculum["credit_hours_total"] == 32
    assert curriculum["course_count_fixed"] is False
    assert curriculum["pathway_details"]["thesis"]["thesis_hours"] == 8
    assert curriculum["pathway_details"]["non_thesis"]["coursework_hours"] == 32
    assert curriculum["internship_required"] is False

    deadlines = {item["round"]["en"]: item["deadline"] for item in uiuc["application_timeline_profile"]["application_rounds"]}
    assert deadlines["Fall MS thesis and full funding consideration"] == "December 1"
    assert deadlines["Fall MS non-thesis"] == "July 1"
    assert deadlines["Spring MS thesis and full funding consideration"] == "October 1"

    assert uiuc["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert uiuc["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert uiuc["data_quality"]["checked_official_source_count"] == 20
    assert uiuc["data_quality"]["unverified_critical_fields"] == []
    assert uiuc["data_quality"]["status"] == "verified"


def test_umich_aero_mse_keeps_language_unknown_and_separates_current_cost_funding_and_housing():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    michigan = dataframe.loc[dataframe["id"] == "umich-aero"].iloc[0]

    eligibility = michigan["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["gre"]["policy"] == "required"
    assert eligibility["gre"]["validity_rule"].startswith("Up to 5 years")
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 90

    language = michigan["language_profile"]
    assert language["teaching_language"] == ["Unknown"]
    assert language["english_required"] is True
    assert language["accepted_english_tests"][0]["minimum_score"] == 84
    assert language["accepted_english_tests"][1]["minimum_score"] == 6.5
    assert language["duolingo_accepted"] is False

    cost = michigan["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_full_time_term_nonresident"] == 34019
    assert cost["tuition_usd_per_year"] == 68038
    assert cost["mandatory_fees_usd_per_year"] == 1493.78
    assert cost["academic_billed_baseline_usd_per_two_terms"] == 69531.78
    assert cost["program_specific_total_cost_of_attendance_usd_per_year"] is None

    funding = michigan["scholarship_profile"]
    assert funding["admission_funding_offer"] is False
    assert funding["automatic_consideration"] is False
    assert funding["separate_application_required"] is True
    assert funding["mse_share_with_gsra_or_gsi_in_a_term"] == 0.06

    living = michigan["living_profile"]
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_application_separate"] is True
    assert living["official_rent_items"][0]["amount_usd_min"] == 1329
    assert living["official_rent_items"][1]["amount_usd_min"] == 861

    curriculum = michigan["curriculum_profile"]
    assert curriculum["credit_hours_total"] == 30
    assert curriculum["course_count_fixed"] is False
    assert curriculum["thesis_required"] is False
    assert curriculum["internship_required"] is False
    assert len(curriculum["tracks"]) == 5

    assert michigan["data_quality"]["status"] == "partial"
    assert michigan["data_quality"]["unverified_critical_fields"] == ["language"]
    assert michigan["quality_control"]["qc_status"] == "needs_revision"
    assert michigan["student_sentiment_profile"]["student_satisfaction_score"] is None


def test_purdue_aae_ms_separates_routes_current_cost_funding_and_graduate_housing():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    purdue = dataframe.loc[dataframe["id"] == "purdue-aae"].iloc[0]

    eligibility = purdue["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["recommended_gpa"] == 3.25
    assert eligibility["recommended_not_minimum"] is True
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 75
    assert eligibility["gre"]["policy"] == "required_with_waivers"
    assert eligibility["gre"]["recommended_scores"]["quantitative"] == 159

    language = purdue["language_profile"]
    assert language["teaching_language"] == ["Unknown"]
    assert language["english_required"] is True
    assert [item["test"] for item in language["accepted_english_tests"]] == [
        "TOEFL iBT",
        "TOEFL Essentials",
        "IELTS Academic",
        "Duolingo English Test",
    ]
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["on_or_after_2026_01_21"]["overall"] == 4.0

    cost = purdue["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_year"] == 29194
    assert cost["housing_and_food_allowance_usd_per_academic_year"] == 16734
    assert cost["total_cost_of_attendance_usd_per_academic_year"] == 49798
    assert cost["health_insurance_required_for_international_students"] is True
    assert cost["health_insurance_premium_usd"] is None
    assert cost["complete_program_cost_usd"] is None

    funding = purdue["scholarship_profile"]
    assert funding["automatic_consideration"] is False
    assert funding["separate_application_required"] is True
    assert funding["admission_funding_guaranteed"] is False
    assert funding["funding_priority_deadline"] == "December 1 for Fall"

    living = purdue["living_profile"]
    assert living["student_housing_available"] is False
    assert living["housing_access"] == "not_offered"
    assert living["housing_access_detail"] == "not_offered_as_general_graduate_option"
    assert living["average_room_rent_usd"] is None

    curriculum = purdue["curriculum_profile"]
    assert curriculum["credit_hours_total"] == 30
    assert curriculum["pathway_details"]["non_thesis"]["course_count"] == 10
    assert curriculum["pathway_details"]["thesis"]["coursework_hours"] == 21
    assert curriculum["pathway_details"]["thesis"]["research_hours_minimum"] == 9
    assert curriculum["thesis_route_available"] is True
    assert curriculum["internship_required"] is False
    assert curriculum["space_systems_engineering_major_delivery"] == "online_only_not_part_of_this_on_campus_record"

    deadlines = {
        item["round"]["en"]: item["deadline"]
        for item in purdue["application_timeline_profile"]["application_rounds"]
    }
    assert deadlines["Fall on-campus — fullest funding consideration"] == "December 1 of the preceding year"
    assert deadlines["Fall on-campus — final programme deadline"] == "March 30 of the same year"
    assert deadlines["Spring on-campus"] == "September 15 of the preceding year"

    assert purdue["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert purdue["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert purdue["data_quality"]["checked_official_source_count"] == 23
    assert purdue["data_quality"]["unverified_critical_fields"] == ["language"]
    assert purdue["data_quality"]["status"] == "partial"


def test_ut_austin_ase_mse_separates_three_routes_current_cost_funding_and_housing():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    texas = dataframe.loc[dataframe["id"] == "ut-austin-ase"].iloc[0]

    eligibility = texas["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["minimum_gpa"] == 3.0
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 90
    assert eligibility["gre"]["policy"] == "required"
    assert eligibility["gre"]["previously_admitted_averages"]["quantitative"] == 168

    language = texas["language_profile"]
    assert language["teaching_language"] == ["Unknown"]
    assert language["english_required"] is True
    assert [item["test"] for item in language["accepted_english_tests"]] == [
        "TOEFL iBT",
        "IELTS Academic",
        "Duolingo English Test",
    ]
    assert language["accepted_english_tests"][0]["minimum_score"] == 79
    assert language["accepted_english_tests"][2]["minimum_score"] == 115

    cost = texas["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_year_min"] == 17312
    assert cost["tuition_usd_per_year_max"] == 19340
    assert cost["total_cost_of_attendance_usd_per_year_min"] == 41880
    assert cost["total_cost_of_attendance_usd_per_year_max"] == 44279
    assert cost["international_i20_total_usd"] == 45487
    assert cost["health_insurance_premium_usd"] is None

    funding = texas["scholarship_profile"]
    assert funding["automatic_consideration"] is True
    assert funding["separate_application_required"] is True
    assert funding["masters_fully_funded"] is False
    assert funding["minimum_ta_gra_stipend_usd_per_year_2026_27"] == 34000

    living = texas["living_profile"]
    assert living["student_housing_available"] is True
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_application_separate"] is True
    assert living["monthly_housing_rent_usd_per_month_min"] == 619.20
    assert living["monthly_housing_rent_usd_per_month_max"] == 1581

    curriculum = texas["curriculum_profile"]
    assert curriculum["credit_hours_total"] == 30
    assert curriculum["pathway_details"]["thesis"]["coursework_hours"] == 24
    assert curriculum["pathway_details"]["thesis"]["research_hours"] == 6
    assert curriculum["pathway_details"]["report"]["coursework_hours"] == 27
    assert curriculum["pathway_details"]["report"]["research_hours"] == 3
    assert curriculum["pathway_details"]["coursework"]["coursework_hours"] == 30
    assert curriculum["thesis_route_available"] is True
    assert curriculum["report_route_available"] is True

    deadlines = {
        item["round"]["en"]: item["deadline"]
        for item in texas["application_timeline_profile"]["application_rounds"]
    }
    assert deadlines["Fall admission"] == "December 1"
    assert deadlines["Spring admission"] == "October 1"
    assert deadlines["Summer admission"] == "December 1"

    assert texas["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert texas["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert texas["data_quality"]["checked_official_source_count"] == 21
    assert texas["data_quality"]["unverified_critical_fields"] == ["language"]
    assert texas["data_quality"]["status"] == "partial"


def test_tamu_aero_ms_keeps_thesis_funding_cost_housing_and_meng_separate():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    tamu = dataframe.loc[dataframe["id"] == "tamu-aero"].iloc[0]

    eligibility = tamu["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["minimum_gpa"] == 3.25
    assert eligibility["faculty_advisor_confirmation_required_before_admission"] is True
    assert eligibility["faculty_funding_confirmation_required_before_admission"] is True
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 148
    assert eligibility["gre"]["policy"] == "not_required"

    language = tamu["language_profile"]
    assert language["teaching_language"] == ["Unknown"]
    assert language["english_required"] is True
    assert [item["test"] for item in language["accepted_english_tests"]] == [
        "TOEFL iBT", "IELTS Academic", "TOEFL Essentials"
    ]
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["test_on_or_after_2026_01_21"]["overall"] == 4.5
    assert language["accepted_english_tests"][1]["minimum_score"] == 6.0

    curriculum = tamu["curriculum_profile"]
    assert curriculum["credit_hours_total"] == 30
    assert curriculum["formal_coursework_credit_hours"] == 21
    assert curriculum["seminar_credit_hours"] == 2
    assert curriculum["research_credit_hours"] == 7
    assert curriculum["thesis_required"] is True
    assert curriculum["advisory_committee_minimum_members"] == 3
    assert curriculum["non_thesis_route_in_this_record"] is False
    assert curriculum["related_non_thesis_degree"] == "Master of Engineering in Aerospace Engineering"

    cost = tamu["cost_profile"]
    assert cost["academic_year"] == "2026"
    assert cost["tuition_usd_per_year"] == 14641
    assert cost["mandatory_fees_usd_per_year"] == 8356
    assert cost["health_insurance_usd_per_year"] == 3023
    assert cost["living_cost_usd_per_year_i20"] == 19995
    assert cost["total_cost_of_attendance_usd_per_year"] == 46015
    assert cost["complete_program_cost_usd"] is None

    funding = tamu["scholarship_profile"]
    assert funding["automatic_consideration"] is True
    assert funding["separate_application_required"] is False
    assert funding["funding_confirmation_required_before_admission"] is True
    assert funding["published_thesis_track_fully_funded_rate_percent"] == 100
    assert funding["funding_package_breakdown_standardized_on_program_page"] is False
    assert funding["university_minimum_gat_gar_gal_stipend_usd_per_month_50_fte"] == 1826
    assert funding["continued_support_guaranteed"] is False

    living = tamu["living_profile"]
    assert living["student_housing_available"] is True
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_application_separate"] is True
    assert living["housing_application_fee_usd"] == 75
    assert living["monthly_housing_rent_usd_per_month_min"] == 931
    assert living["monthly_housing_rent_usd_per_month_max"] == 1863

    deadlines = {
        item["round"]["en"]: item["deadline"]
        for item in tamu["application_timeline_profile"]["application_rounds"]
    }
    assert deadlines["Fall MS funding priority"] == "December 1 of the preceding year"
    assert deadlines["Spring MS funding priority"] == "September 1 of the preceding year"
    assert tamu["application_timeline_profile"]["final_application_deadline"] is None

    assert tamu["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert tamu["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert tamu["data_quality"]["checked_official_source_count"] == 30
    assert tamu["data_quality"]["unverified_critical_fields"] == ["language"]
    assert tamu["data_quality"]["status"] == "partial"


def test_cu_boulder_traditional_ms_keeps_cost_funding_housing_and_proms_separate():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    boulder = dataframe.loc[dataframe["id"] == "cu-boulder-aes"].iloc[0]

    assert boulder["program_name"] == "Master of Science in Aerospace Engineering Sciences (Traditional MS)"
    assert boulder["duration_years"] == 2
    assert boulder["teaching_language"] == ["Unknown"]

    eligibility = boulder["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["international_application_fee_usd"] == 80
    assert eligibility["gre"]["policy"] == "not_accepted"
    assert eligibility["interview_required"] is None

    language = boulder["language_profile"]
    assert language["english_required"] is True
    assert language["accepted_english_tests"][0]["minimum_score"] == 80
    assert language["accepted_english_tests"][2]["minimum_score"] == 6.5
    assert language["medium_of_instruction_letter_accepted"] is False

    curriculum = boulder["curriculum_profile"]
    assert curriculum["total_credit_hours"] == 30
    assert curriculum["typical_course_equivalent"] == 10
    assert curriculum["minimum_5000_level_or_above_credits"] == 24
    assert curriculum["minimum_asen_credits"] == 18
    assert curriculum["thesis_required"] is False
    assert curriculum["thesis_credits"] == 6
    assert len(curriculum["focus_area_requirements"]) == 5
    assert "Professional MS" in curriculum["verification_notes"]["en"]

    cost = boulder["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_semester_full_time_9_or_more_credits"] == 21000
    assert cost["tuition_usd_per_year"] == 42000
    assert cost["mandatory_fees_usd_per_year"] == 890.66
    assert cost["anthem_gold_ship_usd_per_year_fall_and_spring"] == 5296
    assert cost["first_year_direct_university_cost_with_ship_usd"] == 48411.66
    assert cost["complete_program_cost_usd"] is None

    funding = boulder["scholarship_profile"]
    assert funding["application_mode"] == "separate"
    assert funding["automatic_consideration"] is False
    assert funding["department_funding_for_masters_provided"] is False
    assert funding["teaching_facilitator_open_to_ms"] is True
    assert funding["teaching_facilitator_tuition_remission"] is False
    assert funding["funding_guaranteed"] is False

    living = boulder["living_profile"]
    assert living["housing_access"] == "waitlist"
    assert living["housing_application_separate"] is True
    assert living["housing_application_fee_usd"] == 50
    assert living["housing_offer_security_deposit_usd"] == 1000
    assert living["offer_before_classes_guaranteed"] is False
    assert living["monthly_housing_rent_usd_per_month_min"] == 1119
    assert living["monthly_housing_rent_usd_per_month_max"] == 2163

    rounds = {item["intake"]: item for item in boulder["application_timeline_profile"]["application_rounds"]}
    assert rounds["Fall"]["deadline"] == "December 1"
    assert rounds["Spring"]["deadline"] == "October 1"
    assert rounds["Fall"]["late_applications_accepted"] is False

    assert len(boulder["research_profile"]["key_institutes"]) == 5
    assert "Lockheed Martin" in boulder["industry_ecosystem_profile"]["verified_partnerships"]
    assert boulder["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert boulder["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert boulder["data_quality"]["checked_official_source_count"] == 24
    assert boulder["data_quality"]["unverified_critical_fields"] == ["language"]
    assert boulder["data_quality"]["status"] == "partial"


def test_usc_astronautical_ms_preserves_cycle_conflicts_cost_funding_and_housing():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    usc = dataframe.loc[dataframe["id"] == "usc-viterbi"].iloc[0]

    assert usc["program_name"] == "Master of Science in Astronautical Engineering"
    assert usc["duration_years"] == 2
    assert usc["teaching_language"] == ["Unknown"]

    eligibility = usc["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["stem_opt_extension_eligible"] is True
    assert eligibility["recommendation_letter_count"] == 2
    assert eligibility["application_fee_usd"] == 120
    assert eligibility["gre"]["policy"] == "not_required_but_encouraged"
    assert eligibility["gre"]["cycle"] == 2027
    assert eligibility["interview_required"] is None
    assert len(eligibility["official_source_conflicts"]) == 1

    language = usc["language_profile"]
    assert language["english_required"] is True
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["test_on_or_after_2026_01_21"]["overall"] == 4.5
    assert language["accepted_english_tests"][1]["minimum_score"] == 6.5
    assert language["university_wide_admission_minimum_published"] is False
    assert language["medium_of_instruction_only_from_non_anglophone_country_waives_requirement"] is False

    curriculum = usc["curriculum_profile"]
    assert curriculum["credit_hours_total"] == 27
    assert curriculum["typical_three_unit_course_equivalent"] == 9
    assert curriculum["core_units"] == 12
    assert curriculum["core_elective_units"] == 9
    assert curriculum["technical_elective_units"] == 6
    assert curriculum["thesis_required"] is False
    assert curriculum["thesis_option_available_by_request"] is True
    assert curriculum["thesis_option_guaranteed"] is False
    assert len(curriculum["specializations"]) == 6

    cost = usc["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_unit"] == 2742
    assert cost["tuition_usd_complete_27_units_at_2026_27_rate"] == 74034
    assert cost["tuition_and_mandatory_fees_usd_complete_program_example"] == 77777
    assert cost["complete_program_estimate_excluding_health_insurance_usd"] == 108977
    assert cost["complete_program_estimate_with_old_health_sample_usd"] == 116021
    assert cost["health_insurance_current_2026_27_premium_usd"] is None
    assert cost["i20_2026_total_requirement_usd"] == 84093
    assert cost["i20_amount_is_bill"] is False

    funding = usc["scholarship_profile"]
    assert funding["automatic_consideration"] is True
    assert funding["separate_application_required"] is False
    assert funding["deans_scholarship_award_usd_min"] == 10000
    assert funding["deans_scholarship_award_usd_max"] == 30000
    assert funding["non_eu_eligible"] is True
    assert funding["masters_research_assistantships_available"] is False
    assert funding["masters_teaching_assistantships_available"] is False
    assert funding["funding_guaranteed"] is False

    living = usc["living_profile"]
    assert living["student_housing_available"] is True
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_application_separate"] is True
    assert living["housing_application_fee_usd"] == 65
    assert living["monthly_housing_rent_usd_per_month_min"] == 1110
    assert living["monthly_housing_rent_usd_per_month_max"] == 2000

    rounds = {item["intake"]: item for item in usc["application_timeline_profile"]["application_rounds"]}
    assert rounds["Fall 2027 scholarship consideration"]["deadline"] == "2026-12-15"
    assert rounds["Fall 2027 final - program page"]["deadline"] == "2027-02-15"
    assert rounds["Spring 2027 admission"]["deadline"] == "2026-09-15"
    assert usc["application_timeline_profile"]["deadline_source_conflict"]

    assert len(usc["research_profile"]["key_institutes"]) == 4
    assert usc["research_profile"]["individual_lab_place_guaranteed"] is False
    assert usc["industry_ecosystem_profile"]["verified_partnerships"] == []
    assert usc["industry_ecosystem_profile"]["outcomes_are_partnership_evidence"] is False
    assert usc["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert usc["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert usc["data_quality"]["checked_official_source_count"] == 25
    assert usc["data_quality"]["unverified_critical_fields"] == ["language"]
    assert usc["data_quality"]["status"] == "partial"


def test_ucla_aerospace_ms_separates_program_current_gre_cost_funding_and_housing():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    ucla = dataframe.loc[dataframe["id"] == "ucla-mae"].iloc[0]

    assert ucla["program_name"] == "Master of Science in Aerospace Engineering"
    assert ucla["teaching_language"] == ["Unknown"]

    eligibility = ucla["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["minimum_gpa"] == 3.0
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 155
    assert eligibility["duplicate_related_masters_allowed"] is False
    assert eligibility["gre"]["policy"] == "required"
    assert eligibility["gre"]["cycle"] == "2026/2027"
    assert eligibility["gre"]["aerospace_department_code"] == "1601"

    language = ucla["language_profile"]
    assert language["english_required"] is True
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["test_on_or_after_2026_01_21"]["overall"] == 4.5
    assert language["accepted_english_tests"][1]["minimum_score"] == 7.0
    assert language["accepted_english_tests"][0]["mybest_accepted"] is False

    curriculum = ucla["curriculum_profile"]
    assert curriculum["quarter_units_total"] == 36
    assert curriculum["course_count"] == 9
    assert curriculum["graduate_course_count_minimum"] == 5
    assert curriculum["thesis_required"] is False
    assert curriculum["thesis_route_available"] is True
    assert curriculum["capstone_route_available"] is True
    assert len(curriculum["capstone_formats"]) == 4
    assert curriculum["internship_required"] is False
    assert curriculum["duration_quarters_average"] == 5
    assert curriculum["duration_quarters_maximum"] == 9

    cost = ucla["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_year"] == 28242
    assert cost["mandatory_fees_usd_per_year"] == 1861.40
    assert cost["registrar_final_direct_mandatory_charges_usd"] == 36985.40
    assert cost["registrar_nonresident_supplemental_tuition_usd"] == 15102
    assert cost["registrar_ucship_usd"] == 6882
    assert cost["financial_aid_standard_nonresident_coa_usd"] == 76034
    assert cost["total_cost_of_attendance_usd_per_year"] == 76034
    assert cost["financial_aid_coa_is_bill"] is False
    assert cost["complete_program_cost_usd"] is None

    funding = ucla["scholarship_profile"]
    assert funding["automatic_consideration"] is False
    assert funding["separate_application_required"] is True
    assert funding["departmental_financial_support_for_ms_available"] is False
    assert funding["phd_students_fill_nearly_all_ta_positions"] is True
    assert funding["limited_mae_gsr_positions_for_ms"] is True
    assert funding["departmental_funding_guaranteed"] is False

    living = ucla["living_profile"]
    assert living["student_housing_available"] is True
    assert living["housing_access"] == "lottery"
    assert living["housing_application_separate"] is True
    assert living["housing_guaranteed"] is False
    assert living["monthly_housing_rent_usd_per_month_min"] == 1146
    assert living["monthly_housing_rent_usd_per_month_max"] == 3269

    rounds = {item["intake"]: item for item in ucla["application_timeline_profile"]["application_rounds"]}
    assert rounds["Fall 2027"]["deadline"] == "2026-12-01"
    assert rounds["Fall 2027"]["gre_required"] is True

    assert len(ucla["research_profile"]["key_institutes"]) == 7
    assert ucla["research_profile"]["individual_lab_place_guaranteed"] is False
    assert len(ucla["industry_ecosystem_profile"]["verified_partnerships"]) == 1
    assert ucla["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert ucla["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert ucla["data_quality"]["checked_official_source_count"] == 19
    assert ucla["data_quality"]["unverified_critical_fields"] == ["language"]
    assert ucla["data_quality"]["status"] == "partial"


def test_ucsd_aerospace_ms_has_current_deadline_cost_routes_housing_and_visa():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    ucsd = dataframe.loc[dataframe["id"] == "ucsd-mae"].iloc[0]

    assert ucsd["program_name"] == "Master of Science in Engineering Sciences (Aerospace Engineering)"
    assert ucsd["teaching_language"] == ["Unknown"]

    eligibility = ucsd["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["minimum_gpa"] == 3.0
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 155
    assert eligibility["gre"]["policy"] == "optional_not_required"
    assert eligibility["gre"]["cycle"] == "Fall 2027"
    assert eligibility["gre"]["absence_viewed_negatively"] is False

    language = ucsd["language_profile"]
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["new_scale"] == 4.5
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["old_scale"] == 85
    assert language["accepted_english_tests"][2]["minimum_score"] == 7.0
    assert language["accepted_english_tests"][3]["minimum_score"] == 120

    curriculum = ucsd["curriculum_profile"]
    assert curriculum["degree_major_code"] == "MAE-MS-001 / MC75"
    assert curriculum["duration_quarters_minimum"] == 3
    assert curriculum["duration_quarters_maximum"] == 7
    assert curriculum["quarter_units_total"] == 36
    assert curriculum["course_count_plan_ii"] == 9
    assert curriculum["course_count_plan_i"] == 6
    assert curriculum["plan_i"]["research_units_mae_299"] == 12
    assert curriculum["plan_ii"]["comprehensive_component_courses"] == 5
    assert curriculum["plan_ii"]["comprehensive_components_required_to_pass"] == 3
    assert curriculum["internship_required"] is False
    assert curriculum["thesis_route_available"] is True
    assert curriculum["capstone_route_available"] is True

    cost = ucsd["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_year"] == 28824
    assert cost["nonresident_supplemental_tuition_usd_per_year"] == 15102
    assert cost["health_insurance_premium_usd"] == 6660
    assert cost["registrar_nonresident_total_usd"] == 38087.17
    assert cost["first_year_direct_university_cost_with_ship_usd"] == 38294.17
    assert cost["financial_aid_standard_nonresident_coa_off_campus_usd"] == 76821
    assert cost["i20_funding_requirement_usd"] == 73507
    assert cost["complete_program_cost_usd"] is None

    funding = ucsd["scholarship_profile"]
    assert funding["automatic_consideration"] is False
    assert funding["separate_application_required"] is True
    assert funding["ms_students_should_expect_support"] is False
    assert funding["ra_ta_for_ms_rare_and_very_competitive"] is True
    assert funding["ase_remission_covers_nonresident_supplemental_tuition"] is False

    living = ucsd["living_profile"]
    assert living["housing_access"] == "waitlist"
    assert living["housing_application_separate"] is True
    assert living["housing_guaranteed"] is False
    assert living["monthly_housing_rent_usd_per_month_min"] == 1050
    assert living["monthly_housing_rent_usd_per_month_max"] == 2220
    assert living["shore_self_nomination_allowed"] is False

    rounds = {item["intake"]: item for item in ucsd["application_timeline_profile"]["application_rounds"]}
    assert rounds["Fall 2027"]["deadline"] == "2027-01-13"
    assert rounds["Fall 2027"]["gre_required"] is False
    assert ucsd["application_timeline_profile"]["late_applications_accepted"] is False
    assert ucsd["application_timeline_profile"]["i20_expedite_available_for_new_admits"] is False

    assert len(ucsd["research_profile"]["key_institutes"]) == 5
    assert ucsd["research_profile"]["individual_lab_place_guaranteed"] is False
    assert len(ucsd["industry_ecosystem_profile"]["verified_partnerships"]) == 2
    assert ucsd["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert ucsd["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert ucsd["data_quality"]["checked_official_source_count"] == 23
    assert ucsd["data_quality"]["unverified_critical_fields"] == ["language"]
    assert ucsd["data_quality"]["status"] == "partial"


def test_mit_aeroastro_sm_has_current_direct_route_units_cost_funding_housing_and_visa():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    mit = dataframe.loc[dataframe["id"] == "mit-aeroastro"].iloc[0]

    assert mit["program_name"] == "Master of Science in Aeronautics and Astronautics (SM)"
    assert mit["duration_years"] == 2.0
    assert mit["teaching_language"] == ["English"]

    eligibility = mit["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["minimum_gpa"] is None
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 90
    assert eligibility["application_fee_waiver_request_deadline"] == "2026-11-18"
    assert eligibility["gre"]["policy"] == "not_accepted"
    assert eligibility["gre"]["considered_if_submitted"] is False

    language = mit["language_profile"]
    assert language["accepted_english_tests"][0]["minimum_score"] == 100
    assert language["accepted_english_tests"][0]["minimum_score_2026_scale"] == 5.0
    assert language["accepted_english_tests"][1]["minimum_score"] == 7.0
    assert language["accepted_english_tests"][2]["minimum_score"] == 135
    assert language["accepted_english_tests"][3]["minimum_score"] == 190
    assert language["waiver_automatic"] is False

    curriculum = mit["curriculum_profile"]
    assert curriculum["coursework_subject_units"] == 66
    assert curriculum["aeroastro_subject_units_minimum"] == 21
    assert curriculum["thesis_units"] == 24
    assert curriculum["total_units_minimum"] == 90
    assert curriculum["course_count"] is None
    assert curriculum["course_count_fixed"] is False
    assert curriculum["full_time_only"] is True
    assert curriculum["part_time_available"] is False
    assert curriculum["delivery_mode"] == "on_campus"
    assert curriculum["thesis_required"] is True
    assert curriculum["non_thesis_route_available"] is False
    assert curriculum["internship_required"] is False

    cost = mit["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["tuition_usd_per_year"] == 66720
    assert cost["mandatory_fees_usd_per_year"] == 420
    assert cost["health_insurance_premium_usd"] == 5148
    assert cost["first_year_tuition_and_mandatory_fees_usd_example"] == 67140
    assert cost["total_cost_of_attendance_usd_per_year"] == 109017
    assert cost["total_cost_of_attendance_usd_12_month"] == 144315
    assert cost["financial_aid_coa_is_bill"] is False
    assert cost["complete_program_cost_usd"] is None

    funding = mit["scholarship_profile"]
    assert funding["automatic_consideration"] is False
    assert funding["separate_application_required"] is True
    assert funding["funding_guaranteed_at_admission"] is False
    assert funding["proactive_search_expected_after_admission"] is True
    assert funding["most_students_funded_by_ra"] is True
    assert funding["ta_positions_per_year_approximate"] == 20
    assert funding["non_eu_eligible"] is None

    living = mit["living_profile"]
    assert living["housing_access"] == "not_guaranteed"
    assert living["housing_selection_method"] == "self_selection_subject_to_availability"
    assert living["housing_application_separate"] is True
    assert living["housing_guaranteed"] is False
    assert living["monthly_housing_rent_usd_per_month_min"] == 1016
    assert living["monthly_housing_rent_usd_per_month_max"] == 2766

    rounds = {item["intake"]: item for item in mit["application_timeline_profile"]["application_rounds"]}
    assert rounds["Fall 2027"]["opens"] == "2026-09-01"
    assert rounds["Fall 2027"]["deadline"] == "2026-12-01"
    assert rounds["Fall 2027"]["gre_required"] is False
    assert mit["application_timeline_profile"]["spring_admission_available"] is False
    assert mit["application_timeline_profile"]["visa_document_processing_time_business_days_max"] == 10
    assert mit["application_timeline_profile"]["financial_proof_amount"] is None

    assert len(mit["research_profile"]["key_institutes"]) == 8
    assert mit["research_profile"]["individual_lab_place_guaranteed"] is False
    assert mit["industry_ecosystem_profile"]["verified_partnerships"] == []
    assert mit["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert mit["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert mit["data_quality"]["checked_official_source_count"] == 23
    assert mit["data_quality"]["status"] == "partial"


def test_stanford_aa_ms_has_current_units_cost_funding_housing_and_visa():
    root = Path(__file__).parents[1]
    dataframe, _ = load_database_folder(root / "data_base", strict=False)
    stanford = dataframe.loc[dataframe["id"] == "stanford-aa"].iloc[0]

    assert stanford["program_name"] == "Master of Science in Aeronautics and Astronautics"
    assert pd.isna(stanford["duration_years"])
    assert stanford["teaching_language"] == ["English"]
    assert stanford["qs_ranking"] == 2

    eligibility = stanford["eligibility_profile"]
    assert eligibility["eligible_for_non_eu"] is True
    assert eligibility["minimum_gpa"] is None
    assert eligibility["recommendation_letter_count"] == 3
    assert eligibility["application_fee_usd"] == 125
    assert eligibility["gre"]["policy"] == "not_required_and_not_considered"
    assert eligibility["gre"]["considered_if_submitted"] is False

    language = stanford["language_profile"]
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["before_2026_01_21"] == 90
    assert language["accepted_english_tests"][0]["minimum_score_policy"]["on_or_after_2026_01_21"] == 4.5
    assert language["accepted_english_tests"][1]["minimum_score"] == 7.0
    assert language["score_validity_years"] == 2

    curriculum = stanford["curriculum_profile"]
    assert curriculum["quarter_units_total"] == 45
    assert curriculum["duration_quarters_minimum"] == 4
    assert curriculum["duration_quarters_maximum"] == 5
    assert curriculum["course_count"] is None
    assert "45 quarter units" in curriculum["course_count_summary"]["en"]
    assert curriculum["basic_core_breadth_course_count"] == 5
    assert curriculum["advanced_aa_core_course_count"] == 3
    assert curriculum["mathematics_course_count"] == 2
    assert curriculum["technical_elective_course_count_minimum"] == 4
    assert curriculum["thesis_required"] is False
    assert curriculum["research_required"] is False

    cost = stanford["cost_profile"]
    assert cost["academic_year"] == "2026/2027"
    assert cost["engineering_tuition_usd_per_quarter_11_to_18_units"] == 23239
    assert cost["three_quarter_standard_tuition_example_usd"] == 69717
    assert cost["tuition_usd_per_year_at_three_quarters"] == 69717
    assert cost["cardinal_care_usd_per_year"] == 8808
    assert cost["non_tuition_standard_budget_usd_three_quarters"] == 49116
    assert cost["total_coa_usd_three_quarters_example"] == 118833
    assert cost["total_cost_of_attendance_usd_per_year"] == 118833
    assert cost["coa_is_invoice"] is False
    assert cost["complete_program_cost_usd"] is None

    funding = stanford["scholarship_profile"]
    assert funding["application_mode"] == "mixed"
    assert funding["automatic_consideration"] is True
    assert funding["separate_application_required"] is True
    assert funding["funding_guaranteed_at_admission"] is False
    assert funding["first_year_ms_assistantship_rare"] is True
    assert funding["knight_hennessy_any_country"] is True
    assert funding["knight_hennessy_deadline"] == "2026-10-06 13:00 PT"

    living = stanford["living_profile"]
    assert living["housing_access"] == "guaranteed"
    assert living["housing_guarantee_type"] == "conditional_first_year_guarantee"
    assert living["housing_application_separate"] is True
    assert living["housing_guaranteed"] is True
    assert living["fall_2027_housing_deadline"] is None
    assert living["monthly_housing_rent_usd_per_month_min"] == 1203
    assert living["monthly_housing_rent_usd_per_month_max"] == 3014

    rounds = {item["intake"]: item for item in stanford["application_timeline_profile"]["application_rounds"]}
    assert rounds["Autumn 2027"]["deadline"] == "2026-12-01"
    assert rounds["Autumn 2027"]["gre_required"] is False
    assert stanford["application_timeline_profile"]["spring_admission_available"] is False
    assert stanford["application_timeline_profile"]["f1_financial_proof_scope"] == "nine_months"
    assert stanford["application_timeline_profile"]["financial_proof_required_before_i20_or_ds2019"] is True
    assert stanford["application_timeline_profile"]["visa_document_processing_time_business_days"] is None

    assert len(stanford["research_profile"]["key_institutes"]) == 8
    assert stanford["research_profile"]["individual_lab_place_guaranteed"] is False
    assert stanford["industry_ecosystem_profile"]["verified_partnerships"] == []
    assert stanford["student_sentiment_profile"]["student_satisfaction_score"] is None
    assert stanford["student_sentiment_profile"]["sentiment_confidence"] == "low"
    assert stanford["data_quality"]["checked_official_source_count"] == 22
    assert stanford["data_quality"]["status"] == "partial"
