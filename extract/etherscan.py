import pandas as pd
import requests
import os
from base_extractor import BaseExtractor

class EtherscanExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("Etherscan")
        self.api_key = os.getenv("ETHERSCAN_API_KEY", "YourApiKeyToken")
        # Aave V2 aWETH token (great for getting rich deposit/withdraw data)
        self.contract_address = "0x030ba81f1c18d280636f32af80b9aad02da05b3c"

    def extract(self) -> pd.DataFrame:
        """Fetch real ERC20 transfer events from Etherscan"""
        url = "https://api.etherscan.io/api"
        # Pull latest 5000 transactions to give a rich set of real wallets
        params = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": self.contract_address,
            "page": 1,
            "offset": 5000,
            "sort": "desc",
            "apikey": self.api_key
        }
        self.logger.info(f"Fetching Transfer events from Etherscan for {self.contract_address}")
        
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("status") != "1":
                # блин опять апи лагает надо переделать потом
                self.logger.warning(f"Etherscan API returned status 0. Message: {data.get('message')}. Returning limited mock data.")
                return self.generate_mock_data()
                
            transfers = data.get("result", [])
            df = pd.DataFrame(transfers)
            self.logger.info(f"Fetched {len(df)} transactions from Etherscan.")
            return df
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to extract from Etherscan: {e}")
            return self.generate_mock_data()

    def generate_mock_data(self) -> pd.DataFrame:
        self.logger.info("Generating Etherscan mock data for pipeline demonstration.")
        import random
        from datetime import datetime, timedelta
        
        events = []
        mock_wallets = [f"0x{str(i).zfill(40)}" for i in range(1, 101)]
        for i in range(100):
            d = datetime.now() - timedelta(days=random.randint(0, 30))
            events.append({
                "block_timestamp": d.isoformat(),
                "transaction_hash": f"0x{random.randint(0, 16**64):064x}",
                "wallet_address": random.choice(mock_wallets),
                "amount_usd": round(random.uniform(500, 50000), 2),
                "event_type": random.choice(["Deposit", "Deposit", "Withdrawal"])
            })
        return pd.DataFrame(events)
