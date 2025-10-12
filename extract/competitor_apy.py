import pandas as pd
import requests
from bs4 import BeautifulSoup
from base_extractor import BaseExtractor
import json

class CompetitorAPYExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("CompetitorAPY")
        # DefiLlama yields API is open and a standard proxy to demonstrate Scraping APY
        self.url = "https://yields.llama.fi/pools"

    def extract(self) -> pd.DataFrame:
        """Scrape competitor APY rates to analyze Churn Drivers"""
        self.logger.info(f"Scraping competitor APYs from {self.url}")
        
        try:
            # We use requests to get the raw payload
            resp = requests.get(self.url)
            resp.raise_for_status()
            
            # In production Web3, complex SPAs require JSON parsing from Next.js payloads or raw API endpoints.
            data = resp.json()
            pools = data.get("data", [])
            
            # Filter for specific Core Competitors (e.g. Aave V2 Ethereum USDC/WETH)
            competitors = []
            for p in pools:
                if p.get("project") in ["aave-v3", "compound-v3"]:
                    competitors.append({
                        "pull_date": pd.Timestamp.today().date(),
                        "pool_id": p.get("pool"),
                        "project": p.get("project"),
                        "symbol": p.get("symbol"),
                        "chain": p.get("chain"),
                        "apy": float(p.get("apy", 0.0)),
                        "apy_base": p.get("apyBase"),
                        "apy_reward": p.get("apyReward"),
                        "tvl_usd": p.get("tvlUsd")
                    })
            
            df = pd.DataFrame(competitors)
            self.logger.info(f"Scraped {len(df)} competitor markets for APY.")
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to scrape APYs: {e}")
            return self.generate_mock_data()

    def generate_mock_data(self) -> pd.DataFrame:
        self.logger.info("Generating Competitor APY mock data for pipeline demonstration.")
        import random
        from datetime import datetime
        data = []
        for d in range(30):
            date_val = (datetime.now() - pd.Timedelta(days=d)).date()
            for project in ["aave-v3", "compound-v3"]:
                data.append({
                    "pull_date": date_val,
                    "pool_id": f"mock-{project}-weth",
                    "project": project,
                    "symbol": "WETH",
                    "chain": "Ethereum",
                    "apy": round(random.uniform(2.0, 8.0), 2),
                    "apy_base": round(random.uniform(1.0, 5.0), 2),
                    "apy_reward": round(random.uniform(0.5, 3.0), 2),
                    "tvl_usd": random.uniform(10_000_000, 500_000_000)
                })
        return pd.DataFrame(data)
