
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select wallet_address
from "defi_v2"."public_marts"."fct_churn_drivers"
where wallet_address is null



  
  
      
    ) dbt_internal_test