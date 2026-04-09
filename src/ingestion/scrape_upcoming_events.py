from datetime import date
import logging
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.helper_functions import get_latest_event, get_event_details


def scrape_upcoming_events():
    try:
        logging.info("Scraping upcoming events...")

        latest_event = get_latest_event()
        if not latest_event:
            logging.warning("No upcoming events found.")
            return []

        fights = get_event_details(latest_event["url"])
        if not fights:
            logging.warning("No fights found.")
            return []

        logging.info(f"Found {len(fights)} fights.")
        return fights

    except Exception as e:
        logging.error(f"Error scraping upcoming events: {e}")
        raise


def insert_upcoming_events(events, engine):
    if not events:
        return

    today = date.today()

    for e in events:
        e["scrape_date"] = today

    metadata = MetaData()
    table = Table(
        "upcoming_events",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    stmt = (
        insert(table)
        .values(events)
        .on_conflict_do_nothing(
            index_elements=[
                "event_date",
                "fighter1_name",
                "fighter2_name"
            ]
        )
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)

    logging.info(f"Inserted {result.rowcount} upcoming fights.")
