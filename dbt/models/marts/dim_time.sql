with staging as (
    select * from {{ ref('stg_country_population') }}
),

unique_years as (
    select distinct reporting_year
    from staging
    where reporting_year is not null
)

select
    md5(cast(reporting_year as varchar)) as time_id,
    reporting_year as year,
    -- Calculate the decade for grouped analytics
    floor(reporting_year / 10) * 10 as decade
from unique_years