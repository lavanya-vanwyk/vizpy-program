from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator


class PopulationRecord(BaseModel):
    """Data contract representing validated country-level population & internet adoption data."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    country_iso: Annotated[
        str,
        Field(
            min_length=3,
            max_length=3,
            description="ISO 3166-1 alpha-3 standardized country code",
        ),
    ]
    country_name: str = Field(
        min_length=1, max_length=150, description="Country or territory name"
    )
    year: Annotated[
        int,
        Field(
            ge=1960,
            le=2026,
            description="Reporting year",
        ),
    ]
    total_population: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Total national population count (non-negative)",
        ),
    ]
    internet_users_pct: Annotated[
        float | None,
        Field(
            default=None,
            ge=0.0,
            le=100.0,
            description="Internet users as a percentage of total population",
        ),
    ]

    # Audit columns
    ingested_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the record passed pipeline validation",
    )
    source_origin: str = Field(
        default="WorldBank_API",
        description="Identifies the upstream raw collection origin",
    )

    @field_validator("country_iso")
    @classmethod
    def enforce_uppercase_iso(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError(f"Country ISO must contain only letters: '{v}'")
        return v.upper()


class QuarantineRecord(BaseModel):
    """Captures unparseable or out-of-spec raw payloads for dead-letter queuing."""

    raw_payload: dict  # type: ignore
    rejection_reason: str
    quarantined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
