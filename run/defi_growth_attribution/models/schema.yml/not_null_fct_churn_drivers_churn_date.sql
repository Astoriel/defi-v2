
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select churn_date
from "defi_v2"."public_marts"."fct_churn_drivers"
where churn_date is null



  
  
      
    ) dbt_internal_test