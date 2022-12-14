# Snowflake Spreadsheet Uploader

This a demo showcasing various capabilities of Streamlit applications built on Snowflake:
- Directly upload data from spreadsheets (.csv, .xlsx) into Snowflake tables
- Visualisations
- Data & file validation
- Caching / Memoization

## Setup

### Prerequisities

You will need the following:
- Snowflake account. We highly recommend creating a trial account over any production accounts.
- Snowflake role with `CREATE DATABASE` and `CREATE TABLE` privileges. If using a trial account, the `SYSADMIN` role is sufficient for this exercise.

If running this on your own machine, you will need *either*:
- Python3.8
- Docker

Code and deployment has been tested and verified on [Gitpod](https://gitpod.io)

#### Please Note

The Streamlit code creates a few objects within your Snowflake account:
- A Database: `SNOWFLAKE_LAB_ONLINE_RETAIL`
- A Table: `SNOWFLAKE_LAB_ONLINE_RETAIL.PUBLIC.TRANSACTIONS`

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

*(Optional, but recommended)* Create a virtualenv
```
python3 -m venv ./snowflake-csv-uploader-env
source ./snowflake-csv-uploader-env/bin/activate
```

Install required packages:
```
pip3 install -r requirements.txt
```

Run your app
```
streamlit run streamlit_app.py
```

Assuming everything is run and configured correctly, you will be given a URL link to the app running
