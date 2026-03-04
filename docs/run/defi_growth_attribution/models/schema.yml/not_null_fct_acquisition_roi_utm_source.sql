
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select utm_source
from "defi_v2"."public_marts"."fct_acquisition_roi"
where utm_source is null



  
  
      
    ) dbt_internal_test