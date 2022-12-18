import os
import re
import pandas as pd

def pandas_load_wrapper(datapath):
    file_extension = os.path.splitext(os.path.basename(datapath))[1]
    print(file_extension)
    if file_extension == ".csv":
        df = pd.read_csv(datapath)
        df['index'] = range(1, len(df)+1)
        print(df.columns)
        return df
    elif re.match("^\.(xls|xlsx|xlsm|xlsb|odf|ods|odt)$", file_extension):
        print('Excel')
        df = pd.read_excel(datapath)
        print(df)
        return df