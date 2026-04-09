import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
from datetime import datetime
import psycopg2 as pg
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.helper_functions import HEADERS,chunk_dataframe


def scrape_event_urls(limit="ALL"):

    try:
        # Limit parameter for future scraping
        if isinstance(limit, str) and limit != "ALL":
            try:
                limit = int(limit)
            except ValueError:
                raise ValueError("Invalid limit parameter")

        # Scrape Event URLs
        url = "http://ufcstats.com/statistics/events/completed?page=all"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            return (f"Error fetching UFCStats page: {response.status_code}", 500)

        soup = BeautifulSoup(response.content, "lxml")

        rows = [row for row in soup.select("tr.b-statistics__table-row")
        if row.select_one("a.b-link_style_black") 
        and row.select_one("span.b-statistics__date")]

        events = []

        for row in rows:
            # Data Extraction
            a_tag = row.select_one("a.b-link_style_black")
            date_span = row.select_one("span.b-statistics__date")

            # Data Cleaning
            event_url = a_tag["href"].strip().rstrip("/")
            event_title = a_tag.get_text(strip=True)

            try:
                event_date = datetime.strptime(
                    date_span.get_text(strip=True),
                    "%B %d, %Y"
                ).date()
            except Exception as e:
                logging.warning(f"Invalid date format: {e}")
                continue

            events.append((event_url, event_date, event_title))

        if limit != "ALL":
            events = events[:limit]

        # Build DataFrame
        df = pd.DataFrame(events, columns=["event_url", "event_date", "title"])

        # Clean types & formatting
        df["event_url"] = df["event_url"].astype(str).str.strip().str.rstrip("/")
        df["title"] = df["title"].astype(str).str.strip()
        df["event_date"] = pd.to_datetime(df["event_date"]).dt.date

        return df

    except Exception as e:
        logging.error(f"Error scraping event urls: {e}")
        raise


def insert_event_urls(event_urls, engine):
    if event_urls.empty:
        return

    metadata = MetaData()
    table = Table(
        "event_urls",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    stmt = insert(table).values(
        event_urls.to_dict(orient="records")
    ).on_conflict_do_nothing(
        index_elements=["event_url"]
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)

    logging.info(f"Inserted {result.rowcount} new event_urls.")