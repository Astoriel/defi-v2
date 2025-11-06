---
title: DeFi Protocol Analytics
---

# 📊 Web3 Growth Attribution & Churn Intelligence

```sql fct_acquisition_roi
select * from defi_db.fct_acquisition_roi
```

```sql fct_churn_drivers
select * from defi_db.fct_churn_drivers
```

This interactive dashboard tracks Marketing Spend ROAS and Capital Flight against Competitor Yields in real-time.

---

## 🚀 1. Marketing ROAS & TVL Acquisition 

The chart below links off-chain marketing spend (Google & Twitter Ads) with actual on-chain liquidity deposits. *Are we spending money efficiently?*

<BarChart 
    data={fct_acquisition_roi} 
    x=utm_campaign 
    y=total_revenue_usd 
    series=utm_source
    title="Attributed TVL by Campaign"
/>

<DataTable data={fct_acquisition_roi} />

<br/>

## 📉 2. Capital Churn & Competitor APY Correlation

This chart visualizes the correlation between competitor yield offers and capital flight. *When competitors raise their APY, does our TVL drop?*

<LineChart 
    data={fct_churn_drivers} 
    x=churn_date 
    y=top_competitor_apy
    y2=withdrawn_usd
    title="Capital Withdrawn vs Competitor APY"
/>

<DataTable data={fct_churn_drivers} />
