
  create view "defi_v2"."public_staging"."stg_coingecko_prices__dbt_tmp"
    
    
  as (
    -- models/staging/stg_coingecko_prices.sql

with source as (
    select * from "defi_v2"."raw"."coingecko_prices"
),

renamed as (
    select
        date::date as price_date,
        token_id::varchar as token_id,
        price_usd::numeric(18,4) as price_usd
    from source
)

select * from renamed
  );