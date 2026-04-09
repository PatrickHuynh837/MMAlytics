import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, Column, Text, Integer, Boolean, MetaData
from src.ingestion.helper_functions import (
    chunk_dataframe,
    parse_int,
    get_fighter_id,
    get_striking_stats,
    get_grappling_stats,
    scrape_one_fight,
    HEADERS
)
import re



def scrape_fight_stats(engine):
    try:
        fight_stats_df = pd.read_sql_table("fight_stats", engine, schema="raw")
        fight_data_df = pd.read_sql_table("fight_data", engine, schema="raw")

        missing_fights = fight_data_df[
            ~fight_data_df["fight_url"].isin(fight_stats_df["fight_url"])
        ]

        logging.info(f"🟡 Found {len(missing_fights)} fights missing stats")

        all_rows = []
        for url in missing_fights["fight_url"]:
            all_rows.extend(scrape_one_fight(url))

        if not all_rows:
            logging.info("⚠️ No new fight stats scraped")
            return pd.DataFrame()

        df = pd.DataFrame(all_rows)

        # enforce schema here
        int_cols = [
            "knockdowns",
            "total_strikes_att",
            "total_strikes_succ",
            "sig_strikes_att",
            "sig_strikes_succ",
            "takedown_att",
            "takedown_succ",
            "submission_att",
            "reversals",
        ]
        df[int_cols] = df[int_cols].astype("Int64")

        return df

    except Exception as e:
        logging.error(f"❌ Error scraping fight stats: {e}")
        raise


def insert_fight_stats(fight_stats, engine):

    if fight_stats is None or fight_stats.empty:
        logging.info("No new fight stats to insert.")
        return

    try:
        metadata = MetaData()

        fight_stats_table = Table(
            "fight_stats",
            metadata,
            schema="raw",
            autoload_with=engine
        )

        total_inserted = 0

        with engine.begin() as conn:
            for chunk in chunk_dataframe(fight_stats, size=100):
                stmt = (
                    insert(fight_stats_table)
                    .values(chunk.to_dict(orient="records"))
                    .on_conflict_do_nothing(
                        index_elements=["fight_url", "fighter_id"]
                    )
                )

                result = conn.execute(stmt)
                total_inserted += result.rowcount

        logging.info(f"📥 Inserted {total_inserted} new fight_stats rows")

    except Exception as e:
        logging.error(f"❌ Error inserting fight stats: {e}")
        raise
