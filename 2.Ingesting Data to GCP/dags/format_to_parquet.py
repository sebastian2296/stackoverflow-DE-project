import logging
import pandas as pd



def parquetize(src_file, path):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return

    table = pd.read_csv(src_file)
    table.to_parquet(path)
