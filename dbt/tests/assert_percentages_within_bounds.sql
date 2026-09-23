-- Rate must be a valid percentage between 0 and 100.
select
    fact_id,
    geo_id,
    internet_users_pct
from {{ ref('fct_internet_adoption') }}
where internet_users_pct < 0 
   or internet_users_pct > 100