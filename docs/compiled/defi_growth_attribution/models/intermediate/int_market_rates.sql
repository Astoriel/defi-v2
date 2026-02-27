-- models/intermediate/int_market_rates.sql

with rates as (
    select * from "defi_v2"."public_staging"."stg_competitor_apy"
)

select
    rate_date,
    project_name,
    token_symbol,
    avg(apy_percentage) as daily_avg_apy
from rates
group by 1, 2, 3