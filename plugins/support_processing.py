import pandas as pd

class SupportProcessing:
    def __init__(self, dataframe, table_name) -> None:
        self.table_name = table_name
        self.columns = ""
        self.values = ""
        self.odku = ""

        end_col = dataframe.columns[-1]
        for col in dataframe.columns:
            if col == end_col:
                self.columns += col
                self.values += "%s"
                self.odku += col + "=" + "VALUES(" + col + ")"
            else:
                self.columns += col + ", "
                self.values += "%s, "
                self.odku += col + "=" + "VALUES(" + col + "), "
    
    def create_query_insert_into(self):
        create_query = \
            f"INSERT INTO {self.table_name}" + \
            f" ({self.columns}) " + \
            f"VALUES ({self.values}) " + \
            f"ON DUPLICATE KEY UPDATE {self.odku}"
        return create_query
        
