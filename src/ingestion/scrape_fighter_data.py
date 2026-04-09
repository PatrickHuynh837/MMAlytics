import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
from datetime import datetime
import logging
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.helper_functions import HEADERS, scrape_fighter_from_url,chunk_dataframe


def scrape_fighter_data(engine):
    try:
        fighter_urls_df = pd.read_sql_table("fighter_urls", engine, schema="raw")
        fighter_data_df = pd.read_sql_table("fighter_data", engine, schema="raw")

        missing_urls = fighter_urls_df.loc[
            ~fighter_urls_df["fighter_url"].isin(
                fighter_data_df["fighter_url"]
            ),
            "fighter_url"
        ]

        if missing_urls.empty:
            logging.info("No new fighters to scrape.")
            return pd.DataFrame()

        fighter_data = []

        for url in missing_urls:
            data = scrape_fighter_from_url(url)
            if data:
                fighter_data.append(data)

        return pd.DataFrame(fighter_data)

    except Exception as e:
        logging.error(f"Error scraping fighter data: {e}")
        raise


def insert_fighter_data(fighter_data_df, engine):
    if fighter_data_df.empty:
        return

    metadata = MetaData()
    table = Table(
        "fighter_data",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    total_inserted = 0

    with engine.begin() as conn:
        for chunk in chunk_dataframe(fighter_data_df, size=500):
            stmt = insert(table).values(
                chunk.to_dict(orient="records")
            ).on_conflict_do_nothing(
                index_elements=["fighter_url"]
            )
            result = conn.execute(stmt)
            total_inserted += result.rowcount

    logging.info(f"Inserted {total_inserted} new fighter_data.")



