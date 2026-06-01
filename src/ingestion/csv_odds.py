import logging
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.helper_functions import chunk_dataframe


def pull_csv_odds(file_path: str) -> pd.DataFrame:
    # Read CSV safely
    df = pd.read_csv(file_path, low_memory=False)

    # Clean column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Expected columns based on YOUR dataset
    expected_cols = [
        "fighter_1", "fighter_2",
        "odds_1", "odds_2",
        "event_date", "adding_date",
        "source", "region"
    ]

    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    # Clean values
    df["fighter_1"] = df["fighter_1"].astype(str).str.strip()
    df["fighter_2"] = df["fighter_2"].astype(str).str.strip()

    df["odds_1"] = pd.to_numeric(df["odds_1"], errors="coerce")
    df["odds_2"] = pd.to_numeric(df["odds_2"], errors="coerce")

    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce").dt.date
    df["snapshot_time"] = pd.to_datetime(df["adding_date"], errors="coerce")

    df["bookmaker"] = df["source"].astype(str).str.strip()
    df["region"] = df["region"].astype(str).str.strip()

    # Keep only relevant columns for DB
    df = df[[
        "fighter_1",
        "fighter_2",
        "odds_1",
        "odds_2",
        "event_date",
        "snapshot_time",
        "bookmaker",
        "region"
    ]]

    # Drop bad rows
    df = df.dropna(subset=[
        "fighter_1",
        "fighter_2",
        "odds_1",
        "odds_2",
        "event_date",
        "snapshot_time",
        "bookmaker"
    ])

    # Remove duplicates inside dataframe
    df = df.drop_duplicates(subset=[
        "fighter_1",
        "fighter_2",
        "event_date",
        "bookmaker",
        "snapshot_time"
    ])

    if df.empty:
        logging.warning("No valid odds rows after cleaning.")

    return df


def insert_odds_data(odds_data: pd.DataFrame, engine, chunk_size: int = 1000) -> None:
    if odds_data is None:
        logging.info("No odds data provided.")
        return

    if not isinstance(odds_data, pd.DataFrame):
        odds_data = pd.DataFrame(odds_data)

    if odds_data.empty:
        logging.info("Odds DataFrame is empty.")
        return

    metadata = MetaData()
    table = Table(
        "ufc_betting_odds_api",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    total_inserted = 0

    try:
        with engine.begin() as conn:
            for chunk in chunk_dataframe(odds_data, size=chunk_size):
                records = chunk.to_dict(orient="records")

                stmt = (
                    insert(table)
                    .values(records)
                    .on_conflict_do_nothing(
                        index_elements=[
                            "fighter_1",
                            "fighter_2",
                            "event_date",
                            "bookmaker",
                            "snapshot_time"
                        ]
                    )
                )

                result = conn.execute(stmt)
                total_inserted += result.rowcount or 0

        logging.info(f"Inserted {total_inserted} new odds rows.")

    except Exception as e:
        logging.error(f"Error inserting odds data: {e}")
        raise