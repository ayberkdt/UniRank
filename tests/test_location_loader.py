from pathlib import Path

from unirank.core.json_loader import load_database_folder


def test_web_rows_preserve_verified_location_coordinates():
    database = Path(__file__).parents[1] / "data_base"
    dataframe, report = load_database_folder(database, strict=False)

    rows_with_coordinates = [
        row for row in dataframe.to_dict(orient="records")
        if isinstance(row.get("location"), dict)
        and row["location"].get("latitude") is not None
        and row["location"].get("longitude") is not None
    ]

    assert report.records_loaded > 0
    assert rows_with_coordinates, "The API payload must retain map coordinates."
