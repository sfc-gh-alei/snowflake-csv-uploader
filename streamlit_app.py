#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Use 'Getting Started Snowpark Python' Anaconda
# ----------------------------------------------------------------------------
# File Processing in Snowflake via Streamlit
# Person of Contact : Alex Lei (alex.lei@snowflake.com)
# version = '1.0'
#
# Version History:
# V1.0 - AL - 17-OCT-22 - Initial version
# ----------------------------------------------------------------------------

# Packages section
import streamlit as st
import openpyxl as xl
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

# Import Connector for Snowflake Data Cloud!
import snowflake.connector  #upm package(snowflake-connector-python==2.7.0)

# Title information

st.set_page_config(page_title="SnowLabs: CSV File Upload app", page_icon="", layout="centered")

# Make sure session state is preserved
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

st.title("Snowflake Labs: Uploading CSV file into Snowflake")
st.sidebar.text("Connection info:")
st.sidebar.text(f"Account: {st.secrets.snowflake.account}")

# Initialize connection, using st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    con = snowflake.connector.connect(
        user=f"{st.secrets.snowflake.user}",
        password=f"{st.secrets.snowflake.password}",
        account=f"{st.secrets.snowflake.account}",
        role=f"{st.secrets.snowflake.role}",
        warehouse=f"{st.secrets.snowflake.warehouse}",
    )
    con.cursor().execute("USE DATABASE UEBA")
    con.cursor().execute("USE SCHEMA UEBA.PUBLIC")
    return con

#
# Perform query, using st.experimental_memo to only rerun when the query changes or after 10 min.
#
@st.experimental_memo(ttl=600)
def run_query_pandas(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()
conn = init_connection()

#
# Input: Choose a file from Desktop
#

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    #dataframe = xl.load_workbook(uploaded_file)
    # Write the data from the DataFrame to the table named "accounts".
    with st.spinner('Uploading file ...'):
        success, nchunks, nrows, _ = write_pandas(conn, dataframe, 'TRANSACTIONS')
    st.success("Success!")











