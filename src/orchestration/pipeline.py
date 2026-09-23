import subprocess

from prefect import flow, get_run_logger, task

from src.ingestion.world_bank import WorldBankExtractor


@task(retries=2, retry_delay_seconds=10)
def extract_and_load_bronze():
    """Fetches live data from the World Bank API and writes to Parquet."""
    logger = get_run_logger()
    logger.info("Starting World Bank API extraction...")

    extractor = WorldBankExtractor(start_year=2000, end_year=2023)
    records = extractor.extract_and_validate()  # type: ignore
    extractor.save_to_bronze(records)  # type: ignore

    logger.info(f"Successfully loaded {len(records)} records to Bronze Parquet.")


@task
def run_dbt_models():
    """Executes dbt build to transform Bronze -> Silver -> Gold and run tests."""
    logger = get_run_logger()
    logger.info("Starting dbt transformations and data quality tests...")

    # Run dbt build via subprocess
    result = subprocess.run(
        ["dbt", "build", "--project-dir", "dbt", "--profiles-dir", "dbt"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        logger.error(f"dbt build failed:\n{result.stdout}\n{result.stderr}")
        raise RuntimeError("dbt models or tests failed.")

    logger.info("dbt build completed successfully.")
    logger.debug(result.stdout)


@flow(name="Internet Adoption Pipeline", log_prints=True)
def internet_adoption_elt():
    """Main Orchestration Flow"""
    logger = get_run_logger()
    logger.info("Starting the Internet Adoption ELT Pipeline.")

    # Define dependency chain
    extract_and_load_bronze()
    run_dbt_models()

    logger.info("Pipeline completed successfully!")


if __name__ == "__main__":
    # Run the flow locally
    internet_adoption_elt()
