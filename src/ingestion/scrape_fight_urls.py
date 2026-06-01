import logging
import pandas as pd
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert

from src.ingestion.helper_functions import (
    chunk_dataframe,
    get_soup_with_playwright
)


def scrape_fight_urls(engine):
    try:
        events_df = pd.read_sql_table("event_urls", engine, schema="raw")
        fight_df = pd.read_sql_table("fight_urls", engine, schema="raw")

        missing_events_df = events_df[
            ~events_df["event_url"].isin(fight_df["event_url"])
        ]

        if missing_events_df.empty:
            logging.info("No new events to scrape for fight URLs.")
            return pd.DataFrame()

        results = []

        for _, row in missing_events_df.iterrows():
            event_url = row["event_url"]
            title = row["title"]
            date = row["event_date"]

            try:
                soup = get_soup_with_playwright(
                    event_url,
                    parser="lxml",
                    selector="tr.b-fight-details__table-row"
                )

                rows = soup.select("tr.b-fight-details__table-row")

                for tr in rows:
                    cols = tr.find_all("td")

                    if len(cols) < 2:
                        continue

                    fight_tag = cols[0].find("a", href=True)

                    if fight_tag:
                        fight_url = fight_tag["href"].strip()

                        results.append({
                            "event_url": event_url,
                            "title": title,
                            "event_date": date,
                            "fight_url": fight_url
                        })

            except Exception as e:
                logging.warning(f"Scraping error for {event_url}: {e}")
                continue

        if not results:
            return pd.DataFrame()

        return pd.DataFrame(results)

    except Exception as e:
        logging.error(f"Error scraping fight urls: {e}")
        raise


def insert_fight_urls(fight_urls, engine):
    if fight_urls is None or fight_urls.empty:
        logging.info("No new fight URLs to insert.")
        return

    metadata = MetaData()

    fight_urls_table = Table(
        "fight_urls",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    total_inserted = 0

    with engine.begin() as conn:
        for chunk in chunk_dataframe(fight_urls, size=500):
            stmt = insert(fight_urls_table).values(
                chunk.to_dict(orient="records")
            ).on_conflict_do_nothing(
                index_elements=["fight_url"]
            )

            result = conn.execute(stmt)
            total_inserted += result.rowcount

    logging.info(f"Inserted {total_inserted} new fight_urls.")