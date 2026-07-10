from pathlib import Path

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
    assert all("program_name" in row for row in structured_rows)
    assert all("language_profile" in row for row in structured_rows)
