import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.helper_functions import HEADERS



def scrape_rankings():

    ##Meta Rankings
    url = "https://www.ufc.com/rankings"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Failed to fetch rankings page: {e}")
        return []

    soup = BeautifulSoup(response.content, "lxml")
    rankings_data = []
    ranking_date = datetime.utcnow().date()

    ranking_sections = soup.find_all("div", class_="view-grouping")

    logging.info(f"Found {len(ranking_sections)} ranking sections")

    for section in ranking_sections:
        header = section.find("div", class_="view-grouping-header")
        if not header:
            continue

        division = header.get_text(strip=True)

        champion_tag = section.find("div", class_="rankings--athlete--champion")
        if champion_tag:
            champion_name = champion_tag.find("h5").get_text(strip=True)
            rankings_data.append({
                "date": ranking_date,
                "weight_class": division,
                "fighter": champion_name,
                "rank": 0
            })

        fighters = section.find_all("td", class_="views-field views-field-title")
        for rank, fighter in enumerate(fighters, start=1):
            fighter_name = fighter.get_text(strip=True)
            rankings_data.append({
                "date": ranking_date,
                "weight_class": division,
                "fighter": fighter_name,
                "rank": rank
            })

    return rankings_data




def insert_rankings_data(rankings_data, engine):
    if not rankings_data:
        return

    metadata = MetaData()
    table = Table(
        "rankings",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    stmt = (
        insert(table)
        .values(rankings_data)
        .on_conflict_do_nothing(
            index_elements=["date", "weight_class", "fighter"]
        )
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)

    logging.info(f"Inserted {result.rowcount} new ranking rows.")

    