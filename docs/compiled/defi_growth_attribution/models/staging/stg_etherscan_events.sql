-- models/staging/stg_etherscan_events.sql

with source as (
    select * from "defi_v2"."raw"."etherscan_events"
),

renamed as (
    select
        block_timestamp::timestamp as block_timestamp,
        transaction_hash::varchar as tx_hash,
        wallet_address::varchar as wallet_address,
        amount_usd::numeric(18,2) as deposit_amount_usd,
        event_type::varchar as event_type -- 'Deposit' or 'Withdrawal'
    from source
)

select * from renamed