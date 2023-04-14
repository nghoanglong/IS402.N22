import airflow
from airflow import DAG
import pandas as pd
from datetime import timedelta, datetime
from mysql_operators import MySQLOperators
from gsheets_operators import GsheetsOperators

def checking():
    gsheet_op = GsheetsOperators(spreadsheet_id="1lPir7v8VeHBFM5YM8S5JJrrHYMRj5F8ys_asdUZoQ9U")
    sheets = gsheet_op.meta_sheet.get('sheets', '')

    df = gsheet_op.get_value_sheet("Promotion Info")
    # row_id = pd.DataFrame(list(df.index), columns=["row_id"])
    # print(list(df.index))
    # print(row_id)
    df["row_id"] = list(df.index)
    print(df.columns)
    print(df)

if __name__ == '__main__':
    checking()
