import pytest
from pydantic import ValidationError
from src.contracts.population import PopulationRecord


def test_valid_population_record():
    record = PopulationRecord(
        country_iso="zaf",
        country_name="South Africa",
        year=2022,
        total_population=60_000_000,
        internet_users_pct=72.3,
    )
    assert record.country_iso == "ZAF"
    assert record.year == 2022
    assert record.total_population == 60_000_000
    assert record.internet_users_pct == 72.3
    assert record.source_origin == "WorldBank_API"
    assert record.ingested_at is not None


def test_invalid_iso_code_fails():
    with pytest.raises(ValidationError) as exc:
        PopulationRecord(
            country_iso="INVALID",
            country_name="Unknown",
            year=2020,
            total_population=1000,
            internet_users_pct=None,
        )
    assert "country_iso" in str(exc.value)


@pytest.mark.parametrize(
    "bad_year",
    [1950, 2030],
)
def test_out_of_bounds_year_fails(bad_year):
    with pytest.raises(ValidationError) as exc:
        PopulationRecord(
            country_iso="USA",
            country_name="United States",
            year=bad_year,
            total_population=300_000_000,
            internet_users_pct=None,
        )
    assert "year" in str(exc.value)


def test_invalid_percentage_fails():
    with pytest.raises(ValidationError) as exc:
        PopulationRecord(
            country_iso="CAN",
            country_name="Canada",
            year=2021,
            total_population=38_000_000,
            internet_users_pct=105.5,  # Exceeds 100%
        )
    assert "internet_users_pct" in str(exc.value)


def test_negative_population_fails():
    with pytest.raises(ValidationError) as exc:
        PopulationRecord(
            country_iso="DEU",
            country_name="Germany",
            year=2021,
            total_population=-500,
            internet_users_pct=None,
        )
    assert "total_population" in str(exc.value)
