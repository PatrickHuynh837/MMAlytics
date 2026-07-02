from sqlalchemy import create_engine
from src.ingestion.scrape_fight_data import *
from src.ingestion.scrape_fight_urls import *
from src.ingestion.scrape_event_data import *
from src.ingestion.scrape_event_urls import *
from src.ingestion.scrape_fight_stats import *
from src.ingestion.helper_functions import *
from src.ingestion.scrape_fighter_urls import *
from src.ingestion.scrape_fighter_data import *
from src.ingestion.scrape_rankings import *
from src.ingestion.scrape_upcoming_events import *
from src.ingestion.scrape_api_odds import *
from src.ingestion.csv_rankings import *
from src.ingestion.csv_odds import *

import re           

DB_URL = (
    
    "postgresql+psycopg://neondb_owner:npg_Bo2SUY6ngypR@"
    "ep-orange-frost-afcl94sd-pooler.c-2.us-west-2.aws.neon.tech/"
    "neondb?sslmode=require"
  
)

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    force=True
)

def main():


    engine = create_engine(
        DB_URL,
        pool_pre_ping=True,
        pool_recycle=3600
        )

    #Scrape & Insert Event URLs
    df = scrape_event_urls()
    insert_event_urls(df, engine)


    # #Scrape & Insert Event Data
    df = scrape_event_data(df)
    insert_event_data(df, engine)

    #Scrape & Insert Fight URLs
    df = scrape_fight_urls(engine)
    insert_fight_urls(df, engine)

    #Scrape & Insert Fight Data
    df = scrape_fight_data(engine)
    insert_fight_data(df, engine)

    # #Scrape & Insert Fight Stats
    df = scrape_fight_stats(engine)
    insert_fight_stats(df, engine)

    # #   Scrape & Insert Fighter URLs
    df = scrape_fighter_urls()
    insert_fighter_urls(df, engine)

    # #Scrape & Insert Fighter Data
    df = scrape_fighter_data(engine)
    insert_fighter_data(df, engine)

    #Scrape & Insert Rankings
    rankings = scrape_rankings()
    insert_rankings_data(rankings, engine)

    #Scrape & Insert Upcoming Events
    events = scrape_upcoming_events()
    insert_upcoming_events(events, engine)

    #Scrape & Insert CSV Rankings
    # rankings = pull_csv_rankings("src/ingestion/UFC_rankings_history.csv")
    # insert_rankings_data(rankings, engine)

    #Scrape & Insert Odds
    odds = fetch_odds_data()
    insert_odds_data(odds, engine)

    #Scrape & Insert CSV Odds
    # odds = pull_csv_odds("src/ingestion/UFC_betting_odds(1).csv")
    # insert_odds_data(odds, engine)

    

if __name__ == "__main__":
    main()
