import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, Column, Text, Integer, Boolean, MetaData
from src.ingestion.helper_functions import (
    chunk_dataframe,
    get_winner,
    get_info,
    get_event_name,
    get_result_details,
    HEADERS,
    get_soup_with_playwright
)

import re


def scrape_fight_data(engine):
    try:
        logging.info("Starting fight data scraping job.")

        fight_df = pd.read_sql_table(
            "fight_urls",
            engine,
            schema="raw"
        )

        fight_data_df = pd.read_sql_table(
            "fight_data",
            engine,
            schema="raw"
        )

        missing_fights = fight_df[
            ~fight_df["fight_url"].isin(
                fight_data_df["fight_url"]
            )
        ]

        total_to_scrape = len(missing_fights)

        logging.info(f"Fights to scrape: {total_to_scrape}")

        if missing_fights.empty:
            return pd.DataFrame()

        records = []

        for fight_url in missing_fights["fight_url"]:

            logging.info(f"Scraping fight: {fight_url}")

            try:
                soup = get_soup_with_playwright(
                    fight_url,
                    parser="lxml",
                    selector="div.b-fight-details__person"
                )

                fighters = soup.select(
                    "div.b-fight-details__person"
                )

                if len(fighters) != 2:
                    logging.warning(
                        f"Invalid fighter count ({len(fighters)}): "
                        f"{fight_url}"
                    )
                    continue

                f1 = fighters[0].select_one(
                    "h3"
                ).get_text(strip=True)

                f2 = fighters[1].select_one(
                    "h3"
                ).get_text(strip=True)

                f1_url = fighters[0].select_one(
                    "a"
                )["href"]

                f2_url = fighters[1].select_one(
                    "a"
                )["href"]

                winner = get_winner(
                    f1,
                    f2,
                    fighters
                )

                referee = get_info(
                    "Referee:",
                    soup
                )

                finish_round = int(
                    get_info("Round:", soup) or 0
                )

                finish_time = get_info(
                    "Time:",
                    soup
                )

                num_rounds = 0

                time_format = next(
                    (
                        p for p in soup.select(
                            "p.b-fight-details__text"
                        )
                        if "Time format:" in p.text
                    ),
                    None
                )

                if time_format:
                    match = re.search(
                        r"(\d+)\s*Rnd",
                        time_format.text
                    )

                    if match:
                        num_rounds = int(
                            match.group(1)
                        )

                weight_tag = soup.select_one(
                    "i.b-fight-details__fight-title"
                )

                weight_class = (
                    weight_tag.get_text(strip=True)
                    .replace(" Bout", "")
                    if weight_tag
                    else None
                )

                title_fight = bool(
                    weight_class
                    and "Title" in weight_class
                )

                gender = (
                    "F"
                    if weight_class
                    and "Women" in weight_class
                    else "M"
                )

                result = get_info(
                    "Method:",
                    soup
                )

                result_details = get_result_details(
                    soup
                )

                event_name = get_event_name(
                    soup
                )

                records.append({
                    "event_name": event_name,
                    "referee": referee,
                    "f_1": f1,
                    "f_2": f2,
                    "f_1_url": f1_url,
                    "f_2_url": f2_url,
                    "winner": winner,
                    "num_rounds": num_rounds,
                    "title_fight": title_fight,
                    "weight_class": weight_class,
                    "gender": gender,
                    "result": result,
                    "result_details": result_details,
                    "finish_round": finish_round,
                    "finish_time": finish_time,
                    "fight_url": fight_url,
                })

            except Exception as e:
                logging.warning(
                    f"Failed scraping fight "
                    f"{fight_url}: {e}"
                )
                continue

        if not records:
            return pd.DataFrame()

        return pd.DataFrame(records)

    except Exception as e:
        logging.error(f"Error scraping fight data: {e}")
        raise


def insert_fight_data(fight_data, engine):

    if fight_data is None or fight_data.empty:
        logging.info("No new fight data to insert.")
        return

    try:
        metadata = MetaData()

        fight_data_table = Table(
            "fight_data",
            metadata,
            schema="raw",
            autoload_with=engine
        )

        total_inserted = 0

        with engine.begin() as conn:

            for chunk in chunk_dataframe(
                fight_data,
                size=100
            ):

                stmt = (
                    insert(fight_data_table)
                    .values(
                        chunk.to_dict(
                            orient="records"
                        )
                    )
                    .on_conflict_do_nothing(
                        index_elements=["fight_url"]
                    )
                )

                result = conn.execute(stmt)

                total_inserted += result.rowcount

        logging.info(
            f"Inserted {total_inserted} "
            f"new fight_data rows."
        )

    except Exception as e:
        logging.error(
            f"Error inserting fight data: {e}"
        )
        raise

    
