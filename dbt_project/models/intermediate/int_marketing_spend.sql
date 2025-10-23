-- models/intermediate/int_marketing_spend.sql

with google as (
    select
        metric_date,
        utm_source,
        utm_medium,
        campaign_name,
        spend_usd,
        impressions,
        clicks
    from {{ ref('stg_google_ads') }}
),

twitter as (
    select
        metric_date,
        utm_source,
        utm_medium,
        campaign_name,
        spend_usd,
        impressions,
        clicks
    from {{ ref('stg_twitter_ads') }}
)

select * from google
union all
select * from twitter
