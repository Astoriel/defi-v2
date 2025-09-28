from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseExtractor(ABC):
    def __init__(self, name: str):
        self.name = name
        self.db_url = os.getenv("DATABASE_URL", "postgresql://pipeline:pipeline_secret@localhost:5433/defi_pipeline")
        self.engine = create_engine(self.db_url)
        self.logger = logging.getLogger(self.name)

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract data from source and return a pandas DataFrame"""
        pass

    def generate_mock_data(self) -> pd.DataFrame:
        """Generate realistic mock data if USE_MOCK_DATA is enabled or API fails."""
        self.logger.warning(f"Mock data generator not implemented for {self.name}. Returning empty DataFrame.")
        return pd.DataFrame()

    def transform_raw(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply very basic normalizations before loading to raw schema"""
        return df

    def load_to_db(self, df: pd.DataFrame, table_name: str):
        """Load DataFrame into raw schema of PostgreSQL"""
        if df is None or df.empty:
            self.logger.warning(f"No data to load for {table_name}.")
            return
            
        self.logger.info(f"Loading {len(df)} rows into raw.{table_name}")
        
        # Ensure schema exists and clear table safely
        with self.engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            conn.commit()
            try:
                conn.execute(text(f"DELETE FROM raw.{table_name};"))
                conn.commit()
            except Exception:
                pass
            
        df.to_sql(
            table_name,
            self.engine,
            schema="raw",
            if_exists="append", # Appending after manual delete avoids DROP TABLE conflicts
            index=False
        )
        self.logger.info(f"Successfully loaded {table_name}")

    def run(self, table_name: str):
        """Orchestrates extract, transform, load"""
        self.logger.info(f"Starting extraction for {self.name}...")
        
        use_mock = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
        
        if use_mock:
            self.logger.info(f"USE_MOCK_DATA is active. Bypassing API to generate mock data for {self.name}.")
            df = self.generate_mock_data()
        else:
            df = self.extract()
            
        df = self.transform_raw(df)
        self.load_to_db(df, table_name)
        self.logger.info(f"Extraction for {self.name} complete.")
