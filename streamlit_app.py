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
# V1.1 - SK - 21-OCT-22 - Add file path validation, README, docker setup
# V1.2 - SK - 21-OCT-22 - Add 'About' section, dashboards, refined data upload workflow
# ----------------------------------------------------------------------------

# Packages section
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from snowflake.connector.pandas_tools import write_pandas
import plotly.express as px

# Import Connector for Snowflake Data Cloud!
import snowflake.connector  #upm package(snowflake-connector-python==2.7.0)

# Title information
st.set_page_config(page_title="SnowLabs: CSV File Upload app", page_icon="📤", layout="wide")

# Make sure session state is preserved
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

# Initialize connection, using st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    con = snowflake.connector.connect(
        user=f"{st.secrets.snowflake.user}",
        password=f"{st.secrets.snowflake.password}",
        account=f"{st.secrets.snowflake.account}",
        role=f"{st.secrets.snowflake.role}",
        warehouse=f"{st.secrets.snowflake.warehouse}"
    )
    con.cursor().execute("CREATE DATABASE IF NOT EXISTS SNOWFLAKE_LAB_ONLINE_RETAIL")
    con.cursor().execute("USE DATABASE SNOWFLAKE_LAB_ONLINE_RETAIL")
    con.cursor().execute("USE SCHEMA SNOWFLAKE_LAB_ONLINE_RETAIL.PUBLIC")
    con.cursor().execute('''
        CREATE TABLE IF NOT EXISTS TRANSACTIONS (
            invoice varchar,
            stockcode varchar,
            description varchar,
            quantity bigint,
            invoicedate varchar,
            price numeric,
            customerid bigint,
            country varchar
        )
    ''')
    return con

st.title("Snowflake Labs: Uploading spreadsheets into Snowflake")
st.sidebar.header('About')
st.sidebar.write('You can easily extend a Streamlit application beyond simple dashboarding use cases.')
st.sidebar.write('This example application showcases a solution to a use case where a non-technical staff needs to upload spreadsheet data to Snowflake on a regular basis.')

st.sidebar.subheader("Connection info:")
st.sidebar.write(f"Account: {st.secrets.snowflake.account}")

# Initialise tabs
tab1, tab2 = st.tabs(['Upload Data', 'Dashboard'])

#
# Perform query, using st.experimental_memo to only rerun when the query changes or after 15 seconds. Adjust this if you'd like to minimise the number of queries sent to Snowflake
#
@st.experimental_memo(ttl=15)
def run_query_pandas(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()
conn = init_connection()

# Reset data
clear_tbl = st.sidebar.button('Clear Snowflake Table Data')
if clear_tbl:
    conn.cursor().execute("TRUNCATE TABLE TRANSACTIONS")


#
# Upload Tab
#
with tab1:
    uploaded_file = st.file_uploader("Choose a file. Accepted file types: .csv, .xlsx")
    if uploaded_file is not None:
        # When a file is uploaded, a UploadedFile class object is returned.
        # The UploadedFile class is a subclass of BytesIO, and therefore it is "file-like". This means you can pass them anywhere where a file is expected.
        file_name = uploaded_file.name
        if not file_name.endswith(('.csv', '.xlsx')):
            st.error('Wrong file type. Make sure it is one of: .csv, .xlsx')
        else:
            data_type_map = {
                'INVOICE': 'str',
                'STOCKCODE': 'str',
                'DESCRIPTION': 'str',
                'QUANTITY': 'int64',
                'INVOICEDATE': 'str',
                'PRICE': 'float64',
                'CUSTOMERID': 'int64',
                'COUNTRY': 'str'
            }
            if file_name.endswith('.csv'):
                # Can be used wherever a "file-like" object is accepted:
                df = pd.read_csv(uploaded_file, dtype=data_type_map)
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, dtype=data_type_map)

            # We can validate the inputs against the column specs
            if sorted(list(df.columns)) != sorted(list(data_type_map.keys())):
                st.error('Mismatch in columns. Check the inputs and try again.')
            else:
                st.success('Data looks good. Review the data below and click \'Upload\' to send data to Snowflake ❄️', icon="✅")
                upload_btn = st.button('Upload')
                if upload_btn:
                    with st.spinner('Uploading file ...'):
                        success, nchunks, nrows, _ = write_pandas(conn, df, 'TRANSACTIONS')
                    st.success("Success!", icon="✅")

            # Generate a table of the data that's been staged for the uploader to view 
            st.subheader("Data Preview")
            AgGrid(df)

#
# Dashboards Tab
#
with tab2:
    invoice_agg = run_query_pandas('''
        SELECT
            COUNT(DISTINCT INVOICE) as num_invoices
            , COUNT(DISTINCT stockcode) as num_skus
            , COUNT(DISTINCT country) as num_countries
        FROM TRANSACTIONS
    ''')

    rev_by_country = run_query_pandas('''
        SELECT
            COUNTRY
            , SUM(PRICE * QUANTITY) as revenue
        FROM TRANSACTIONS
        GROUP BY COUNTRY
    ''')

    top_products = run_query_pandas('''
        SELECT
            DESCRIPTION as product_name
            , SUM(PRICE * QUANTITY) as revenue
        FROM TRANSACTIONS
        GROUP BY DESCRIPTION
        ORDER BY revenue DESC
        LIMIT 5
    ''')

    # You can organise visualisations into columns:
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Invoices", invoice_agg['NUM_INVOICES'])
    col2.metric("Number of SKUs", invoice_agg['NUM_SKUS'])
    col3.metric("Number of Countries", invoice_agg['NUM_COUNTRIES'])

    # We can utilise other plotting packages, such as plotly:
    pie_fig = px.pie(rev_by_country, values='REVENUE', names='COUNTRY', title = 'Revenue by Country')
    top_custs = px.bar(top_products, x='PRODUCT_NAME', y='REVENUE')

    col4, col5 = st.columns(2)
    col4.plotly_chart(pie_fig, use_container_width=True)
    col5.plotly_chart(top_custs, use_container_width=True)













