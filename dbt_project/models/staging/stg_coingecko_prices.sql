-- models/staging/stg_coingecko_prices.sql

with source as (
    select * from {{ source('raw_data', 'coingecko_prices') }}
),

renamed as (
    select
        date::date as price_date,
        token_id::varchar as token_id,
        price_usd::numeric(18,4) as price_usd
    from source
)

select * from renamed
