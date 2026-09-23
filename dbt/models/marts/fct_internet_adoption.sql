with staging as (
    select * from {{ ref('stg_country_population') }}
),

geography as (
    select * from {{ ref('dim_geography') }}
),

time_dim as (
    select * from {{ ref('dim_time') }}
),

fact_build as (
    select
        md5(s.iso_code || cast(s.reporting_year as varchar)) as fact_id,
        g.geo_id,
        t.time_id,
        s.total_population,
        s.internet_users_pct,
        
        -- Derived Metric: Absolute internet user count
        cast(
            (s.total_population * (s.internet_users_pct / 100.0)) as bigint
        ) as internet_users_count,

        -- Window Function: Calculate percentage point change from the previous year
        s.internet_users_pct - lag(s.internet_users_pct) over (
            partition by s.iso_code 
            order by s.reporting_year
        ) as yoy_pct_point_change

    from staging s
    left join geography g on s.iso_code = g.iso_code
    left join time_dim t on s.reporting_year = t.year
)

select * from fact_build