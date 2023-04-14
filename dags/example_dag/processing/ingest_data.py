import airflow
from airflow import DAG
import pandas as pd
from datetime import timedelta, datetime
from mysql_operators import MySQLOperators
from gsheets_operators import GsheetsOperators
import numpy as np

def ingest_data():
    query_data = """
            SELECT *
            FROM brands;
        """
    df_b = MySQLOperators("db_connection").get_data_to_pd(query_data)
    data = (
        df_b.replace({"": None})
        .replace({np.nan: None})
        .to_records(index=False)
        .tolist()
    )

    MySQLOperators("dwh_connection").insert_dataframe_into_table("brands_ingested", df_b, data)

    return True

if __name__ == '__main__':
    ingest_data()
