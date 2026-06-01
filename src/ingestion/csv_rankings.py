import logging
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from src.ingestion.helper_functions import chunk_dataframe





def pull_csv_rankings(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    # Basic cleanup
    df.columns = [col.strip().lower() for col in df.columns]

    # Ensure expected columns exist
    expected_cols = ["date", "weight_class", "fighter", "rank"]
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    # Keep only needed columns
    df = df[expected_cols].copy()

    # Clean values
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["weight_class"] = df["weight_class"].astype(str).str.strip()
    df["fighter"] = df["fighter"].astype(str).str.strip()
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce").astype("Int64")

    # Drop bad rows
    df = df.dropna(subset=["date", "weight_class", "fighter", "rank"])

    # Optional: remove duplicates inside the dataframe itself
    df = df.drop_duplicates(subset=["date", "weight_class", "fighter"])

    return df


def insert_rankings_data(rankings_data: pd.DataFrame, engine, chunk_size: int = 1000) -> None:
    if rankings_data is None:
        logging.info("No rankings data provided.")
        return

    if not isinstance(rankings_data, pd.DataFrame):
        rankings_data = pd.DataFrame(rankings_data)

    if rankings_data.empty:
        logging.info("Rankings DataFrame is empty.")
        return

    metadata = MetaData()
    table = Table(
        "rankings",
        metadata,
        schema="raw",
        autoload_with=engine
    )

    total_inserted = 0

    try:
        with engine.begin() as conn:
            for chunk in chunk_dataframe(rankings_data, size=chunk_size):
                records = chunk.to_dict(orient="records")

                stmt = (
                    insert(table)
                    .values(records)
                    .on_conflict_do_nothing(
                        index_elements=["date", "weight_class", "fighter"]
                    )
                )

                result = conn.execute(stmt)
                total_inserted += result.rowcount or 0

        logging.info(f"Inserted {total_inserted} new ranking rows.")

    except Exception as e:
        logging.error(f"Error inserting rankings data: {e}")
        raise