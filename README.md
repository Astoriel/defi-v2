# 📊 Web3 Growth & Churn Intelligence Pipeline

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![dbt](https://img.shields.io/badge/dbt-PostgreSQL-FF694B.svg)
![Evidence](https://img.shields.io/badge/Evidence.dev-BI-brightgreen.svg)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg)

> An End-to-End Modern Data Stack (MDS) pipeline designed to solve two of the biggest problems in Web3 Marketing: **Off-chain to On-chain Attribution (ROAS)** and **Yield-Driven Capital Flight (Churn).**

---

## 🚀 View Live Dashboards

The analytics artifacts are automatically built via CI/CD and hosted on GitHub Pages:
- 📈 **[Evidence BI Dashboard](https://astoriel.github.io/defi-v2/)**: Interactive ROAS & Churn visualizations.
- 🗄️ **[dbt Data Dictionary](https://astoriel.github.io/defi-v2/docs/)**: Full DAG lineage, schema documentation, and Kimball modeling constraints.

---

## ⚡ Modular API Toggles & "Mock Mode"

To make it easy to evaluate and test this project without needing 6 different active API keys (Google Ads, Twitter API, Etherscan Pro, Posthog, etc.), this repository uses **Fully Autonomous Extractors**.

You can toggle **any** individual module via your `.env` file (e.g., `ENABLE_GOOGLE_ADS=false`). The pipeline handles missing configurations elegantly—if a module is disabled, the Python runner will automatically fallback to generating a localized mock dataframe for that specific data source. This guarantees the `dbt` Data Warehouse DAG compiles perfectly every time, even if you run it with only 1 or 2 live APIs.

Alternatively, by setting `USE_MOCK_DATA=true` globally, the pipeline bypasses all live API calls and generates a beautifully synchronized portfolio-ready dataset for local viewing in minutes.

*Note: This repository is the v2 evolution of my earlier [DeFi-Pipeline-PoC](https://github.com/Astoriel/DeFi-Pipeline-PoC). This version introduces strict Kimball dimensional modeling, automated CI/CD testing, and an Evidence.dev BI layer.*

---

## 📖 Architecture Overview

```mermaid
graph TD
    %% Data Sources
    subgraph Raw Data Extraction [Python Extractors]
        G[Google Ads API] -. Optional .-> EXT(Base Extractor)
        T[Twitter Ads API] -. Optional .-> EXT
        PH[PostHog API] -. Optional .-> EXT
        E[Etherscan RPC] --> EXT
        CG[CoinGecko Price API] --> EXT
        CA[Web Scraper: Comp. APY] --> EXT
    end

    %% Database Layer
    subgraph Data Warehouse [PostgreSQL Server]
        EXT --> RAW[(Raw Staging Tables)]
    end

    %% dbt Transforms
    subgraph dbt Transformations [dbt Core]
        RAW --> STG(stg_models)
        STG --> INT(int_models)
        INT --> FCT1[(fct_acquisition_roi)]
        INT --> FCT2[(fct_churn_drivers)]
    end

    %% BI Presentation 
    subgraph BI Presentation [Evidence.dev]
        FCT1 --> EB[Evidence BI Engine]
        FCT2 --> EB
        EB --> GP[GitHub Pages Static Site]
    end
    
    %% Mock Data Route
    MD[Mock Data Generator] -. Overrides / Fallback .-> EXT
```

The pipeline ingests data from 6 separate sources, transforms it using Kimball dimensional modeling in a PostgreSQL Warehouse, and serves it statically.

### 1. Data Extraction (Python)
- **Web2 Marketing:** Google Ads API (v20), Twitter Ads API
- **Web3 Blockchain:** Etherscan RPC (ERC-20 Transfers)
- **Product Analytics:** PostHog API (Wallet Connections)
- **DeFi Markets:** CoinGecko (Token Prices), Web Scraping (Competitor APY)

### 2. Transformation (dbt)
Models are separated into `staging`, `intermediate`, and `marts`. We output two core fact tables:
- `fct_acquisition_roi`: Links marketing spend to on-chain TVL deposits (True ROAS).
- `fct_churn_drivers`: Correlates capital withdrawals with competitor yield spikes.

<p align="center">
  <img src="assets/dbt_lineage.png" alt="dbt DAG Architecture" width="800">
</p>

### 3. Business Intelligence (Evidence.dev)
We use Evidence (BI-as-code) to generate static Markdown-based analytics pages directly from the `marts` schema. 
*(Visual dashboards available via the [Live Dashboard Link](https://astoriel.github.io/defi-v2/))*

---

## 🛠️ Local Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/astoriel/defi-v2.git
   cd defi-v2
   ```

2. **Setup Environment:**
   Review `.env.example` and set up your local `.env`. Ensure mock mode is enabled:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5434/defi_v2
   USE_MOCK_DATA=true
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Full Pipeline (Extract & Build):**
   ```bash
   # Load mock data to PostgreSQL
   python extract/run_extraction.py
   
   # Run dbt transformations & tests
   cd dbt_project
   dbt build --profiles-dir .
   ```

5. **View Dashboards locally:**
   ```bash
   cd ../reports
   npm install
   npm run build
   npm run preview
   ```

---
*Created as a demonstration of Web3 Data Engineering capabilities.*
