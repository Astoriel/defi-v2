
  create view "defi_v2"."public_staging"."stg_google_ads__dbt_tmp"
    
    
  as (
    -- models/staging/stg_google_ads.sql

with source as (
    select * from "defi_v2"."raw"."google_ads"
),

renamed as (
    select
        date::date as metric_date,
        campaign_id::varchar as campaign_id,
        campaign_name::varchar as campaign_name,
        utm_source::varchar as utm_source,
        utm_medium::varchar as utm_medium,
        cost_usd::numeric(10,2) as spend_usd,
        impressions::int as impressions,
        clicks::int as clicks
    from source
)

select * from renamed
  );