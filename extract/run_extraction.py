import logging
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file before anything else
load_dotenv()

# Ensure current directory is in PYTHONPATH for direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google_ads import GoogleAdsExtractor
from twitter_ads import TwitterAdsExtractor
from posthog_attribution import PostHogExtractor
from etherscan import EtherscanExtractor
from coingecko import CoinGeckoExtractor
from competitor_apy import CompetitorAPYExtractor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RunExtraction_Real")

def main():
    logger.info("Initializing Web3 Growth Analytics Pipeline - 100% Real API Extraction Phase")
    
    # 1. Instantiate Real API Extractors
    google = GoogleAdsExtractor()
    twitter = TwitterAdsExtractor()
    posthog = PostHogExtractor()
    etherscan = EtherscanExtractor()
    coingecko = CoinGeckoExtractor()
    apy_scraper = CompetitorAPYExtractor()
    
    # 2. Extract & Load Marketing Spend Data
    if os.getenv("ENABLE_GOOGLE_ADS", "true").lower() == "true":
        google.run("google_ads")
    else:
        logger.info("Google Ads extraction is DISABLED in config.")

    if os.getenv("ENABLE_TWITTER_ADS", "true").lower() == "true":
        twitter.run("twitter_ads")
    else:
        logger.info("Twitter Ads extraction is DISABLED in config.")
    
    # 3. Extract & Load The Attribution Linkage
    if os.getenv("ENABLE_POSTHOG", "true").lower() == "true":
        posthog.run("posthog_events")
    else:
        logger.info("PostHog Analytics extraction is DISABLED in config.")
    
    # 4. Extract & Load On-Chain and Alternative Data
    etherscan.run("etherscan_events")
    coingecko.run("coingecko_prices")
    apy_scraper.run("competitor_apy")
    
    logger.info("100% REAL Extraction Phase Complete! All available live API data loaded to raw PostgreSQL schema.")

if __name__ == "__main__":
    main()
