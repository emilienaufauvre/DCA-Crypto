import pandas as pd
import glob
import os

from _global import *


if __name__ == '__main__':
    df = pd.DataFrame()

    for filename in glob.glob(os.path.join(PATH_OUTPUT, "*.csv")):
        df = pd.concat([df, pd.read_csv(filename)])

    df = pd.pivot_table(df, 
                        index=[COL_NAME], values=[COL_PUR1, COL_PUR2, 
                                                  COL_AMO1, COL_AMO2],
                        aggfunc="sum")
    df.loc["TOTAL"] = df.sum()
    print(df.to_markdown())

