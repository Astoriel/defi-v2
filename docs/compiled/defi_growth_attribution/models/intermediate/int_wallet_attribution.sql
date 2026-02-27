-- models/intermediate/int_wallet_attribution.sql

with events as (
    select * from "defi_v2"."public_staging"."stg_posthog_events"
    where wallet_address is not null
),

-- Standard First-Touch Attribution model for wallets connecting to DApp
first_touch as (
    select
        wallet_address,
        utm_source,
        utm_medium,
        utm_campaign,
        min(event_timestamp) as first_connected_at
    from events
    group by 1, 2, 3, 4
)

select * from first_touch