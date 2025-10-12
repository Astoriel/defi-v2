import pandas as pd
import requests
import os
from base_extractor import BaseExtractor

class CoinGeckoExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("CoinGecko")
        self.api_key = os.getenv("COINGECKO_API_KEY", "")
        self.coin_id = "ethereum" # Primary asset in our pool

    def extract(self) -> pd.DataFrame:
        """Fetch historical daily prices from CoinGecko to convert TVL to USD"""
        url = f"https://api.coingecko.com/api/v3/coins/{self.coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "30",
            "interval": "daily"
        }
        
        headers = {}
        if self.api_key:
            headers["x-cg-demo-api-key"] = self.api_key
            
        self.logger.info(f"Fetching historical prices for {self.coin_id}")
        
        try:
            resp = requests.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            
            prices = data.get("prices", [])
            df = pd.DataFrame(prices, columns=["timestamp_ms", "price_usd"])
            
            # Convert timestamp to date
            df["date"] = pd.to_datetime(df["timestamp_ms"], unit="ms").dt.date
            df["token_id"] = self.coin_id
            
            self.logger.info(f"Fetched {len(df)} days of pricing data.")
            return df
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to extract from CoinGecko: {e}")
            return self.generate_mock_data()

    def generate_mock_data(self) -> pd.DataFrame:
        self.logger.info("Generating CoinGecko mock data for pipeline demonstration.")
        import random
        from datetime import datetime, timedelta
        data = []
        base_price = 3000.0
        for i in range(30):
            d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            base_price = base_price * random.uniform(0.95, 1.05)
            data.append({
                "timestamp_ms": int((datetime.now() - timedelta(days=i)).timestamp() * 1000),
                "price_usd": round(base_price, 2),
                "date": d,
                "token_id": self.coin_id
            })
        return pd.DataFrame(data)
