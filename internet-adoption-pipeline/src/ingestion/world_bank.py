import requests
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from pydantic import ValidationError

from src.contracts.population import PopulationRecord, QuarantineRecord


class WorldBankExtractor:
    BASE_URL = "http://api.worldbank.org/v2/country/all/indicator"

    def __init__(self, start_year: int = 2000, end_year: int = 2023):
        self.start_year = start_year
        self.end_year = end_year
        # Indicators: Population (Total) and Internet Users (% of pop)
        self.indicators = {
            "population": "SP.POP.TOTL",
            "internet_pct": "IT.NET.USER.ZS",
        }

    def fetch_indicator(self, indicator_code: str) -> dict:
        """Fetches data from the World Bank API with a high per_page limit."""
        url = f"{self.BASE_URL}/{indicator_code}"
        params = {
            "format": "json",
            "date": f"{self.start_year}:{self.end_year}",
            "per_page": 10000,  # Pull large batches to minimize pagination logic
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        if len(data) < 2:
            return {}

        # Map into a dictionary keyed by (country_iso, year)
        parsed_data = {}
        for item in data[1]:
            if item.get("countryiso3code"):  # Skip regional aggregates without ISO3
                key = (item["countryiso3code"], int(item["date"]))
                parsed_data[key] = {
                    "country_name": item["country"]["value"],
                    "value": item["value"],
                }
        return parsed_data

    def extract_and_validate(self) -> list[dict]:
        """Merges indicators, passes them through Pydantic, and returns valid dicts."""
        print("Fetching Total Population data...")
        pop_data = self.fetch_indicator(self.indicators["population"])

        print("Fetching Internet Usage data...")
        net_data = self.fetch_indicator(self.indicators["internet_pct"])

        valid_records = []
        quarantine = []

        # Merge the datasets
        for (iso, year), pop_info in pop_data.items():
            net_val = net_data.get((iso, year), {}).get("value")

            raw_payload = {
                "country_iso": iso,
                "country_name": pop_info["country_name"],
                "year": year,
                "total_population": pop_info["value"],
                "internet_users_pct": net_val,
            }

            try:
                # Enforce the Data Contract
                validated = PopulationRecord(**raw_payload)
                valid_records.append(validated.model_dump())
            except ValidationError as e:
                # Quarantine bad data instead of crashing the pipeline
                q_rec = QuarantineRecord(
                    raw_payload=raw_payload, rejection_reason=str(e)
                )
                quarantine.append(q_rec)

        print(
            f"Validated {len(valid_records)} records. Quarantined {len(quarantine)} records."
        )
        return valid_records

    def save_to_bronze(
        self, valid_records: list[dict], output_dir: str = "data/bronze/internet_usage"
    ):
        """Writes validated records to Parquet partitioned by year."""
        if not valid_records:
            print("No valid records to write.")
            return

        table = pa.Table.from_pylist(valid_records)

        # Write to partitioned parquet files (e.g., year=2020/...)
        pq.write_to_dataset(
            table,
            root_path=output_dir,
            partition_cols=["year"],
            use_dictionary=True,
            compression="snappy",
        )
        print(f"Successfully wrote Parquet partitions to {output_dir}")


if __name__ == "__main__":
    extractor = WorldBankExtractor(start_year=2000, end_year=2023)
    records = extractor.extract_and_validate()
    extractor.save_to_bronze(records)
