import pandas as pd

def get_df():
    return pd.read_csv('base-des-lieux-et-des-equipements-culturels.csv', delimiter=';', header=0, low_memory=False)
