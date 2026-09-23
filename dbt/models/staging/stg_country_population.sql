with raw_source as (
    select * from {{ source('world_bank_bronze', 'internet_usage') }}
),

cleaned as (
    select
        country_iso as iso_code,
        country_name,
        cast(year as integer) as reporting_year,
        cast(total_population as bigint) as total_population,
        cast(internet_users_pct as decimal(5,2)) as internet_users_pct,
        ingested_at,
        source_origin
    from raw_source
    
    where country_iso is not null
),

deduplicated as (
    select *
    from cleaned
    -- Handle API duplicates 
    -- by keeping most recent ingested record
    qualify row_number() over (
        partition by iso_code, reporting_year 
        order by ingested_at desc
    ) = 1
)

select * from deduplicated