from bs4 import BeautifulSoup
import logging
import pandas as pd
from datetime import datetime, date
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.browser import get_page


def scrape_event_data(event_urls):

    rows = []

    with get_page(headless=True) as page:

        for url in event_urls["event_url"]:

            try:
                logging.info(f"Scraping event data: {url}")

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=5000
                )

                page.wait_for_selector(
                    "h2.b-content__title",
                    timeout=3000
                )

                html = page.content()

                soup = BeautifulSoup(html, "lxml")

                event_name_tag = soup.find(
                    "h2",
                    class_="b-content__title"
                )

                details_box = soup.find(
                    "div",
                    class_="b-list__info-box"
                )

                if not event_name_tag:
                    logging.warning(
                        f"Missing event name for {url}"
                    )
                    continue

                event_name = event_name_tag.text.strip()

                event_date = None
                location_city = None
                location_state = None
                location_country = None

                if details_box:

                    for li in details_box.find_all("li"):

                        text = li.get_text(
                            " ",
                            strip=True
                        )

                        if "Date" in text:

                            date_text = (
                                text
                                .split("Date:")[1]
                                .strip()
                            )

                            event_date = datetime.strptime(
                                date_text,
                                "%B %d, %Y"
                            ).date()

                        elif "Location" in text:

                            location_text = (
                                text
                                .split("Location:")[1]
                                .strip()
                            )

                            parts = [
                                p.strip()
                                for p in location_text.split(",")
                            ]

                            location_city = (
                                parts[0]
                                if len(parts) >= 1
                                else None
                            )

                            location_state = (
                                parts[1]
                                if len(parts) >= 2
                                else None
                            )

                            location_country = (
                                parts[2]
                                if len(parts) >= 3
                                else None
                            )

                if event_date and event_date > date.today():
                    continue

                rows.append({
                    "event_url": url,
                    "event_name": event_name,
                    "event_date": (
                        event_date.isoformat()
                        if event_date
                        else None
                    ),
                    "location_city": location_city,
                    "location_state": location_state,
                    "location_country": location_country
                })

            except Exception as e:

                logging.error(
                    f"Unexpected error scraping {url}: {e}"
                )

                continue

    return pd.DataFrame(rows)


def insert_event_data(event_data, engine):

    if event_data.empty:
        logging.warning(
            "No event data to insert."
        )
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

    logging.info(
        f"Inserted {result.rowcount} new event_data rows."
    )