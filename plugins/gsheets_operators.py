import logging
from hooks.GoogleAPI import GoogleAPI
from googleapiclient.discovery import build
import pandas as pd
import numpy as np



class GsheetsOperators:
    def __init__(self, spreadsheet_id="1lPir7v8VeHBFM5YM8S5JJrrHYMRj5F8ys_asdUZoQ9U"):
        self.spreadsheet_id = spreadsheet_id
        self.scopes_sheet = ["https://www.googleapis.com/auth/spreadsheets"]
        try:
            self.con_sheet = GoogleAPI("sheets", self.scopes_sheet)
        except:
            logging.INFO("something wrong with Google API")
        self.service = build("sheets", "v4", credentials=self.con_sheet.creds, cache_discovery=False)
        self.meta_sheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        self.sheet = self.service.spreadsheets().values()
    
    def get_value_sheet(self, range_name):
        # Call the Sheets API
        result = self.sheet.get(spreadsheetId=self.spreadsheet_id, range=range_name).execute()

        values = result.get("values", [])
        df = pd.DataFrame(values)
        # Choose the first row is header columns
        df.columns = df.iloc[0, :]
        # and remove the first row
        df = df.iloc[1:]
        return df

    def clear_data_sheet(self, range_name):
        # Call the Sheets API
        self.sheet.clear(spreadsheetId=self.spreadsheet_id, range=range_name).execute()
        logging.INFO("clear sheet success")
    
    def append_data_sheet(self, data_frame, range_name):
        # Convert data_frame to body format
        data_import = data_frame.to_numpy().tolist()

        # If data_import empty is pass
        if not data_import:
            logging.INFO("Do not new data to update.")
        else:
            value_range_body = {"values": data_import}
            request = self.sheet.append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=value_range_body,
            ).execute()
        return request

    def update_data_sheet(self, data_frame, range_name):
        # Convert data_frame to body format
        columns = data_frame.columns.tolist()
        data_import = data_frame.to_numpy().tolist()

        data_import = np.vstack([columns, data_import]).tolist()

        # If data_import empty is pass
        if not data_import:
            logging.INFO("Do not new data to update.")
        else:
            value_range_body = {"values": data_import}
            request = self.sheet.update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=value_range_body,
            ).execute()
            # Check result append
            if self.spreadsheet_id == request["spreadsheetId"]:
                if request["updatedColumns"] == len(data_import[0]):
                    if request["updatedRows"] == len(data_import):
                        logging.INFO("Update data on sheet completed.")
                    else:
                        logging.ERROR("updated rows != need update rows")
                else:
                    logging.ERROR("updated columns != need update columns")
            else:
                logging.ERROR("updated sheet != need update sheet")

    def HMD_product_ggsheet(self, range_name):
        result = (
            self.sheet.get(spreadsheetId=self.spreadsheet_id, range=range_name).execute()
        )
        values = result.get("values", [])
        hmd_product = pd.DataFrame(values)
        # Choose the first row is header columns
        hmd_product.columns = hmd_product.iloc[0, :]
        # and remove the first row
        hmd_product = hmd_product.iloc[1:]
        # filter rows that the column sku is empty
        hmd_product = hmd_product[hmd_product.product_sku.notnull()]
        product_sku, asin, product_name, group_name, brand = [], [], [], [], []
        for idx, row in hmd_product.iterrows():
            if ("B" in row["fbm"]) and (len(row["fbm"]) == 10):
                asin.append(row["fbm"])
                product_sku.append(row["product_sku"])
                product_name.append(row["product_name"])
                group_name.append(row["group_name"])
                brand.append(row["brand"])
            elif ("B" in row["avc"]) and (len(row["avc"]) == 10):
                asin.append(row["avc"])
                product_sku.append(row["product_sku"])
                product_name.append(row["product_name"])
                group_name.append(row["group_name"])
                brand.append(row["brand"])
        hmd_product_new = pd.DataFrame(
            {
                "product_sku": product_sku,
                "asin": asin,
                "product_name": product_name,
                "group_name": group_name,
                "brand": brand,
            }
        )
        return hmd_product_new
    
    