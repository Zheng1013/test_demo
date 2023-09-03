import pandas as pd
from pathlib import Path

df_path = Path(__file__).resolve().parent / 'prod_name.csv'

def serch_article(itemid):
    df = pd.read_csv(df_path)
    matched_rows = df[df['article_id'].isin(itemid)]
    prod_data = matched_rows['prod_name'].values.tolist()
    grap_data = matched_rows['graphical_appearance_name'].values.tolist()
    return prod_data,grap_data