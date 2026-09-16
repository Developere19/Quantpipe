import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_database_connection():
    """
    Create and return a connection to the QuantPipe PostgreSQL database.
    """
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    return connection

def create_market_data_table():
    """
    Create the market_data table if it does not already exist.
    """
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open DOUBLE PRECISION NOT NULL,
            high DOUBLE PRECISION NOT NULL,
            low DOUBLE PRECISION NOT NULL,
            close DOUBLE PRECISION NOT NULL,
            volume BIGINT NOT NULL,
            daily_return DOUBLE PRECISION,
            price_anomaly BOOLEAN NOT NULL,
            volume_anomaly BOOLEAN NOT NULL,
            PRIMARY KEY (symbol, date)
        );
    """)

    connection.commit()

    cursor.close()
    connection.close()


def insert_market_data(
    df,
    symbol: str
) -> None:
    """
    Insert processed market data into the PostgreSQL market_data table.
    """
    connection = get_database_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO market_data (
            symbol,
            date,
            open,
            high,
            low,
            close,
            volume,
            daily_return,
            price_anomaly,
            volume_anomaly
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, date) DO NOTHING;
    """

    for date, row in df.iterrows():
        cursor.execute(
            insert_query,
            (
                symbol,
                date.date(),
                float(row["open"]),
                float(row["high"]),
                float(row["low"]),
                float(row["close"]),
                int(row["volume"]),
                (
                    None
                    if row["daily_return"] != row["daily_return"]
                    else float(row["daily_return"])
                ),
                bool(row["price_anomaly"]),
                bool(row["volume_anomaly"]),
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_market_data_table()
    print("market_data table created successfully.")

