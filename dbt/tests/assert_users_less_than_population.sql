-- An internet user count cannot exceed the total population of the country.
select
    fact_id,
    geo_id,
    internet_users_count,
    total_population
from {{ ref('fct_internet_adoption') }}
where internet_users_count > total_population