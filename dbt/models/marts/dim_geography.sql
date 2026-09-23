with staging as (
    select * from {{ ref('stg_country_population') }}
),

unique_geography as (
    select distinct
        iso_code,
        country_name
    from staging
)

select
    md5(iso_code) as geo_id,
    iso_code,
    country_name
from unique_geography