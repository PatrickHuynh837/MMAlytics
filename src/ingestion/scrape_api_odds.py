import requests
import logging
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert


API_KEY = "52db7e441b2ddea45f7e6634da0e6124"  # Insert your TheOddsAPI key here

BOOKMAKER_REGIONS = {
    "DraftKings": "us",
    "FanDuel": "us",
    "BetMGM": "us",
    "BetUS": "us",
    "BetOnline.ag": "us",
    "BetRivers": "us",
    "BetAnySports": "us",
    "888sport": "uk",
    "Betfair": "uk",
    "Betway": "uk",
    "Paddy Power": "uk",
    "Virgin Bet": "uk",
    "Grosvenor": "uk",
    "LiveScore Bet": "uk",
    "Matchbook": "uk",
    "Unibet": "eu",
    "Unibet (FR)": "eu",
    "Unibet (NL)": "eu",
    "Betclic (FR)": "eu",
    "LeoVegas": "eu",
    "Marathon Bet": "eu",
    "Nordic Bet": "eu",
    "Coolbet": "eu",
    "Betsson": "eu"
}


def fetch_odds_data(snapshot_time=None):
    url = "https://api.the-odds-api.com/v4/sports/mma_mixed_martial_arts/odds"
    params = {
        "regions": "us,uk,eu",
        "markets": "h2h",
        "oddsFormat": "decimal",
        "apiKey": API_KEY
    }

    if snapshot_time is None:
        snapshot_time = datetime.now(timezone.utc)

    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Odds API request failed: {e}")
        return pd.DataFrame()

    data = res.json()
    rows = []

    for match in data:
        commence_time = match.get("commence_time")
        event_date = None
        if commence_time:
            try:
                event_date = datetime.fromisoformat(
                    commence_time.replace("Z", "+00:00")
                ).date()
            except ValueError:
                logging.warning(f"Could not parse commence_time: {commence_time}")
                event_date = None

        for bookmaker in match.get("bookmakers", []):
            bookmaker_name = bookmaker.get("title")
            region = BOOKMAKER_REGIONS.get(bookmaker_name, "unknown")

            for market in bookmaker.get("markets", []):
                if market.get("key") != "h2h":
                    continue

                outcomes = market.get("outcomes", [])
                if len(outcomes) != 2:
                    continue

                fighter_1 = outcomes[0].get("name")
                odds_1 = outcomes[0].get("price")
                fighter_2 = outcomes[1].get("name")
                odds_2 = outcomes[1].get("price")

                if not fighter_1 or not fighter_2:
                    continue

                rows.append({
                    "fighter_1": fighter_1,
                    "fighter_2": fighter_2,
                    "odds_1": odds_1,
                    "odds_2": odds_2,
                    "event_date": event_date,
                    "snapshot_time": snapshot_time,
                    "bookmaker": bookmaker_name,
                    "region": region
                })

    odds_data = pd.DataFrame(rows)

    if odds_data.empty:
        logging.info("No odds data fetched from API.")
        return odds_data

    return odds_data


def insert_odds_data(odds_data, engine):
    if odds_data.empty:
        logging.info("No odds data to insert.")
        return

    metadata = MetaData()
    table = Table(
        "ufc_betting_odds_api",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    records = odds_data.to_dict(orient="records")

    stmt = insert(table).values(records).on_conflict_do_nothing(
        index_elements=[
            "fighter_1",
            "fighter_2",
            "event_date",
            "bookmaker",
            "snapshot_time",
        ]
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)

    logging.info(f"Inserted {result.rowcount} new odds snapshot rows.")

    