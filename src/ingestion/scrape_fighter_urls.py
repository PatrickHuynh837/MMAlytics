import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
from datetime import datetime
import logging
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
import string
from src.ingestion.helper_functions import chunk_dataframe, HEADERS






def scrape_fighter_urls():
    try:
        fighter_urls = []

        for letter in string.ascii_lowercase:
            url = f"http://ufcstats.com/statistics/fighters?char={letter}&page=all"
            logging.info(f"Scraping fighters for letter: {letter}")

            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")
            rows = [
                row for row in soup.select("tr.b-statistics__table-row")
                if row.select_one("a.b-link_style_black")
            ]

            for row in rows:
                a_tag = row.select_one("a.b-link_style_black")
                fighter_urls.append(
                    a_tag["href"].strip().rstrip("/")
                )

        df = pd.DataFrame(fighter_urls, columns=["fighter_url"])
        df["fighter_url"] = df["fighter_url"].astype(str).str.strip().str.rstrip("/")
        df = df.drop_duplicates()

        return df

    except Exception as e:
        logging.error(f"Error scraping fighter urls: {e}")
        raise




def insert_fighter_urls(fighter_urls_df, engine):
    if fighter_urls_df.empty:
        return
    try:
        metadata = MetaData()
        table = Table(
            "fighter_urls",
            metadata,
            schema="raw",
            autoload_with=engine
        )

        total_inserted = 0
        
        with engine.begin() as conn:
            for chunk in chunk_dataframe(fighter_urls_df, size=1000):
                stmt = insert(table).values(
                    chunk.to_dict(orient="records")
                ).on_conflict_do_nothing(
                    index_elements=["fighter_url"]
                )
                result = conn.execute(stmt)
                total_inserted += result.rowcount

        
    except Exception as e:
        logging.info(f"Inserted {total_inserted} new fighter_urls.")
        raise
    