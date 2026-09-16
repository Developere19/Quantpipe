# Quantpipe
# QuantPipe

QuantPipe is a fault-tolerant market data pipeline built in Python that automatically collects daily stock-market data, validates its quality, detects unusual price and volume movements, and stores processed observations in PostgreSQL.

The project focuses on data reliability and operational resilience. It includes automated validation, anomaly detection, idempotent database writes, retry handling for temporary network failures, transaction rollback, persistent logging, automated testing, and scheduled execution.

## Pipeline Architecture

Market Data API  
↓  
Python Ingestion  
↓  
Data Validation  
↓  
Anomaly Detection  
↓  
PostgreSQL Storage  
↓  
Logging & Monitoring  

The pipeline can be executed manually through a command-line interface or automatically using Windows Task Scheduler.

## Key Features

- Retrieves daily OHLCV market data from Alpha Vantage
- Standardizes API responses into Pandas DataFrames
- Validates missing values, duplicate dates, positive prices, volume, and OHLC relationships
- Detects unusual daily price movements and trading volume
- Stores processed observations in PostgreSQL
- Prevents duplicate records using a composite `(symbol, date)` primary key
- Retries temporary HTTP/network failures
- Rolls back failed database transactions
- Records pipeline execution and failures using persistent logging
- Supports arbitrary stock symbols through a command-line interface
- Supports automated daily execution
- Includes an automated pytest test suite

## Project Structure

```text
Quantpipe/
├── src/
│   ├── ingestion.py
│   ├── validation.py
│   ├── anomaly_detection.py
│   ├── database.py
│   ├── logger.py
│   └── pipeline.py
├── tests/
│   ├── test_ingestion.py
│   ├── test_validation.py
│   ├── test_anomaly_detection.py
│   ├── test_database.py
│   └── test_pipeline.py
├── run_quantpipe.bat
├── requirements.txt
├── .env.example
└── README.md


## Installation

### 1. Clone the repository

git clone <your GitHub repo>
cd Quantpipe

### 2. Create a virtual environment

Using Python 3.12:

py -3.12 -m venv .venv

Activate it on Windows:

.\.venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt

## Configuration

Create a `.env` file in the project root using `.env.example` as a template.

The file should contain:

ALPHA_VANTAGE_API_KEY=your_api_key_here

DB_HOST=localhost
DB_PORT=5432
DB_NAME=quantpipe
DB_USER=your_database_user
DB_PASSWORD=your_database_password

The `.env` file is excluded from version control so API keys and database credentials are not committed to the repository.

## PostgreSQL Setup

Create a PostgreSQL database named `quantpipe`.

The pipeline automatically creates the required `market_data` table if it does not already exist.

Each market observation is uniquely identified by the combination of stock symbol and trading date. Duplicate observations are ignored during repeated pipeline runs.

## Running QuantPipe

Run the pipeline for a stock symbol:

python -m src.pipeline AAPL

For example:

python -m src.pipeline IBM

## Automated Testing

Run the complete test suite with:

python -m pytest -v

## Scheduling

On Windows, `run_quantpipe.bat` can be used with Windows Task Scheduler to run the pipeline automatically.