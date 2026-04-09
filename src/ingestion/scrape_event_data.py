import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
from datetime import datetime
import psycopg2 as pg
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.helper_functions import HEADERS





def scrape_event_data(event_urls):
    rows = []

    for url in event_urls["event_url"]:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            event_name = soup.find("h2", class_="b-content__title").text.strip()
            details_box = soup.find("div", class_="b-list__info-box")

            event_date = None
            location_city = None
            location_state = None
            location_country = None

            if details_box:
                for li in details_box.find_all("li"):
                    if "Date" in li.text:
                        date_text = li.text.split(":")[1].strip()
                        event_date = datetime.strptime(date_text, "%B %d, %Y").date()

                    if "Location" in li.text:
                        location_text = li.text.split("Location:")[1].strip()
                        parts = [p.strip() for p in location_text.split(",")]
                        location_city = parts[0] if len(parts) >= 1 else None
                        location_state = parts[1] if len(parts) >= 2 else None
                        location_country = parts[2] if len(parts) >= 3 else None

            rows.append({
                "event_url": url,
                "event_name": event_name,
                "event_date": event_date.isoformat() if event_date else None,
                "location_city": location_city,
                "location_state": location_state,
                "location_country": location_country
            })

        except requests.HTTPError as e:
            logging.warning(f"Skipping event URL due to HTTP error: {url} ({e})")
            continue

        except Exception as e:
            logging.error(f"Unexpected error scraping {url}: {e}")
            continue

    return pd.DataFrame(rows)


def insert_event_data(event_data, engine):
    if event_data.empty:
        return

    metadata = MetaData()
    table = Table(
        "event_data",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    stmt = insert(table).values(
        event_data.to_dict(orient="records")
    ).on_conflict_do_nothing(
        index_elements=["event_url"]
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)

    logging.info(f"Inserted {result.rowcount} new event_data rows.")







