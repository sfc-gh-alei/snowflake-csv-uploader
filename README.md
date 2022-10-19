# snowflake-csv-uploader
Snowflake CSV file uploader

## Setup

### Prerequisities

You will need the following:
- Snowflake account. We highly recommend creating a trial account over any production accounts.
- Snowflake role with `CREATE DATABASE` privilege. If using a trial account, the `SYSADMIN` role is sufficient for this demo.

### Credentials

Make a copy of the included `./.streamlit/secrets_example.toml` file:
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
streamlit run FileProcess.py
```

Assuming everything is run and configured correctly, you will be given a URL link to the app running
