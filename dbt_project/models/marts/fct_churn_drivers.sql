-- models/marts/fct_churn_drivers.sql

with withdrawals as (
    select * from {{ ref('stg_etherscan_events') }}
    where event_type = 'Withdrawal'
),
rates as (
    select * from {{ ref('int_market_rates') }}
),
max_rates_per_day as (
    -- Find the highest competitor APY for each day to see if they beat us
    select 
        rate_date,
        project_name as top_competitor_name,
        daily_avg_apy as top_competitor_apy
    from (
        select 
            rate_date,
            project_name,
            daily_avg_apy,
            row_number() over (partition by rate_date order by daily_avg_apy desc) as rnk
        from rates
    ) ranked
    where rnk = 1
),
attribution as (
    select * from {{ ref('int_wallet_attribution') }}
)

select
    w.block_timestamp::date as churn_date,
    w.wallet_address,
    w.deposit_amount_usd as withdrawn_usd,
    a.utm_source as original_acquisition_channel,
    a.utm_campaign as original_campaign,
    r.top_competitor_name,
    r.top_competitor_apy
from withdrawals w
left join attribution a on w.wallet_address = a.wallet_address
left join max_rates_per_day r on r.rate_date = w.block_timestamp::date
