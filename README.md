# 📊 Web3 Growth & Churn Intelligence Pipeline

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![dbt](https://img.shields.io/badge/dbt-PostgreSQL-FF694B.svg)
![Evidence](https://img.shields.io/badge/Evidence.dev-BI-brightgreen.svg)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg)

> An End-to-End Modern Data Stack (MDS) pipeline designed to solve two of the biggest problems in Web3 Marketing: **Off-chain to On-chain Attribution (ROAS)** and **Yield-Driven Capital Flight (Churn).**

---

## 🚀 View Live Dashboards

The analytics artifacts are automatically built via CI/CD and hosted on GitHub Pages:
- 📈 **[Evidence BI Dashboard](https://astoriel.github.io/defi-v2/dashboard/)**: Interactive ROAS & Churn visualizations.
- 🗄️ **[dbt Data Dictionary](https://astoriel.github.io/defi-v2/)**: Full DAG lineage, schema documentation, and Kimball modeling constraints.

---

## ⚡ Mock Mode (Zero Setup Required)

To make it easy to evaluate and test this project without needing 6 different active API keys (Google Ads, Twitter API, Etherscan Pro, Posthog, etc.), this repository includes a built-in **Data Generation Engine**.

By simply setting `USE_MOCK_DATA=true` in your `.env` file, the Python extractors will bypass real API endpoints and generate statistically realistic internal and on-chain events. This allows you to compile the entire dbt warehouse and view the BI dashboards locally in minutes.

*Note: This repository is the v2 evolution of my earlier [DeFi-Pipeline-PoC](https://github.com/Astoriel/DeFi-Pipeline-PoC). This version introduces strict Kimball dimensional modeling, dbt testing, and an Evidence.dev BI layer.*

---

## 📖 Architecture Overview

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
*(Visual dashboards available via the [Live Dashboard Link](https://astoriel.github.io/defi-v2/dashboard/))*

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
