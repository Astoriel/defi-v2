-- models/staging/stg_posthog_events.sql

with source as (
    select * from "defi_v2"."raw"."posthog_events"
),

renamed as (
    select
        timestamp::timestamp as event_timestamp,
        distinct_id::varchar as user_session_id,
        event::varchar as event_name,
        wallet_address::varchar as wallet_address,
        utm_source::varchar as utm_source,
        utm_medium::varchar as utm_medium,
        utm_campaign::varchar as utm_campaign
    from source
)

select * from renamed