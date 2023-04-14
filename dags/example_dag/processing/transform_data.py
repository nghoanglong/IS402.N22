import airflow
from airflow import DAG
import pandas as pd
from datetime import timedelta, datetime
from mysql_operators import MySQLOperators
from gsheets_operators import GsheetsOperators
import numpy as np

def transform_data():
    query_data = """
            SELECT *
            FROM brands_ingested;
        """
    df_b = MySQLOperators("dwh_connection").get_data_to_pd(query_data)
    df_b["published"] = df_b["published"] + df_b["brand_owner_id"]

    data = (
        df_b.replace({"": None})
        .replace({np.nan: None})
        .to_records(index=False)
        .tolist()
    )
    MySQLOperators("dwh_connection").insert_dataframe_into_table("brands_transformed", df_b, data)

    return True

if __name__ == '__main__':
    transform_data()
