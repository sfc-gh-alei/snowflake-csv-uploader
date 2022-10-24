# snowflake-csv-uploader
Snowflake CSV file uploader

## Setup

### Prerequisities

You will need the following:
- Snowflake account. We highly recommend creating a trial account over any production accounts.
- Snowflake role with `CREATE DATABASE` privilege. If using a trial account, the `SYSADMIN` role is sufficient for this exercise.

### Set up Snowflake

You will need to create a new database and table for the application to run. Log-on to your Snowflake account and run the following SQL:
```
create database if not exists UEBA;
use schema UEBA.public;

create table if not exists transactions (
    invoice varchar,
    stockcode varchar,
    description varchar,
    quantity bigint,
    invoicedate varchar,
    price numeric,
    customerid bigint,
    country varchar
);
```

### Set up Credentials

This sets up the connection from your Streamlit app to your Snowflake account. Make a copy of the included `./.streamlit/secrets_example.toml` file:
```
cp ./.streamlit/secrets_example.toml ./.streamlit/secrets.toml
```
Substitute each value with values applicable for your Snowflake demo account

## Running your Streamlit Application

### Option 1: Python on Docker

Simply build & run the image with the following:

```
docker build -f Dockerfile -t snowflake-csv-uploader .

# Run
docker run -it \
    -p 8501:8501 \
    -v "$PWD":/app \
    -w /app \
    snowflake-csv-uploader
```

Assuming everything is run and configured correctly, you will be given a URL link to the app running. 

### Option 2: Python

Install required packages via:
```
pip install -r requirements.txt
```

Run your app
```
streamlit run streamlit_app.py
```

Assuming everything is run and configured correctly, you will be given a URL link to the app running
