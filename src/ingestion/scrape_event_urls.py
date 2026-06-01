from bs4 import BeautifulSoup
import logging
import pandas as pd
from datetime import datetime, date
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert

from src.ingestion.helper_functions import (
    chunk_dataframe,
    get_soup_with_playwright
)


def scrape_event_urls(limit="ALL"):

    try:
        if isinstance(limit, str) and limit != "ALL":
            try:
                limit = int(limit)
            except ValueError:
                raise ValueError("Invalid limit parameter")

        url = "http://ufcstats.com/statistics/events/completed?page=all"

        soup = get_soup_with_playwright(
            url,
            parser="lxml",
            selector="tr.b-statistics__table-row"
        )

        rows = [
            row for row in soup.select("tr.b-statistics__table-row")
            if row.select_one("a.b-link_style_black")
            and row.select_one("span.b-statistics__date")
        ]

        print(f"Rows found: {len(rows)}")

        events = []

        for row in rows:

            a_tag = row.select_one("a.b-link_style_black")
            date_span = row.select_one("span.b-statistics__date")

            event_url = a_tag["href"].strip().rstrip("/")
            event_title = a_tag.get_text(strip=True)

            try:
                event_date = datetime.strptime(
                    date_span.get_text(strip=True),
                    "%B %d, %Y"
                ).date()

                if event_date > date.today():
                    continue

            except Exception as e:
                logging.warning(f"Invalid date format: {e}")
                continue

            events.append(
                (
                    event_url,
                    event_date,
                    event_title
                )
            )

        print(f"Events after filtering: {len(events)}")

        if limit != "ALL":
            events = events[:limit]

        df = pd.DataFrame(
            events,
            columns=[
                "event_url",
                "event_date",
                "title"
            ]
        )

        df["event_url"] = (
            df["event_url"]
            .astype(str)
            .str.strip()
            .str.rstrip("/")
        )

        df["title"] = (
            df["title"]
            .astype(str)
            .str.strip()
        )

        df["event_date"] = (
            pd.to_datetime(df["event_date"])
            .dt.date
        )

        return df

    except Exception as e:
        logging.error(f"Error scraping event urls: {e}")
        raise


def insert_event_urls(event_urls, engine):

    if event_urls.empty:
        logging.warning("No event URLs to insert.")
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

    logging.info(
        f"Inserted {result.rowcount} new event_urls."
    )