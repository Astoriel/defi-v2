-- models/staging/stg_competitor_apy.sql

with source as (
    select * from "defi_v2"."raw"."competitor_apy"
),

renamed as (
    select
        pull_date::date as rate_date,
        project::varchar as project_name,
        symbol::varchar as token_symbol,
        apy::numeric(10,4) as apy_percentage
    from source
)

select * from renamed