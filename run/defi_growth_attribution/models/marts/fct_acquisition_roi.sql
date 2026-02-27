
  
    

  create  table "defi_v2"."public_marts"."fct_acquisition_roi__dbt_tmp"
  
  
    as
  
  (
    -- models/marts/fct_acquisition_roi.sql

with attribution as (
    select * from "defi_v2"."public_intermediate"."int_wallet_attribution"
),
spend as (
    select * from "defi_v2"."public_intermediate"."int_marketing_spend"
),
deposits as (
    select * from "defi_v2"."public_staging"."stg_etherscan_events"
    where event_type = 'Deposit'
),

wallet_deposits as (
    select
        d.wallet_address,
        min(d.block_timestamp) as first_deposit_time,
        sum(d.deposit_amount_usd) as total_deposited_usd
    from deposits d
    group by 1
),

attributed_deposits as (
    select
        a.utm_source,
        a.utm_medium,
        a.utm_campaign,
        count(distinct w.wallet_address) as unique_depositors,
        sum(w.total_deposited_usd) as total_revenue_usd
    from attribution a
    join wallet_deposits w on a.wallet_address = w.wallet_address
    group by 1, 2, 3
),

campaign_roas as (
    select
        s.utm_source,
        s.utm_medium,
        s.campaign_name as utm_campaign,
        sum(s.spend_usd) as total_spend_usd,
        sum(s.clicks) as total_clicks
    from spend s
    group by 1, 2, 3
)

select
    c.utm_source,
    c.utm_medium,
    c.utm_campaign,
    c.total_spend_usd,
    c.total_clicks,
    coalesce(ad.unique_depositors, 0) as acquired_users,
    coalesce(ad.total_revenue_usd, 0) as total_revenue_usd,
    case 
        when c.total_spend_usd > 0 then coalesce(ad.total_revenue_usd, 0) / c.total_spend_usd 
        else 0 
    end as roas
from campaign_roas c
left join attributed_deposits ad 
    on c.utm_source = ad.utm_source
    and c.utm_campaign = ad.utm_campaign
  );
  