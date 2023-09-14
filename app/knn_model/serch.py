import pandas as pd
from pathlib import Path
import random

serch_path = Path(__file__).resolve().parent / 'prod_name.csv'


def serch_article(similar_ids):
    df = pd.read_csv(serch_path)
    matched_rows = df[df['article_id'].isin(similar_ids)]
    matched_rows = matched_rows.set_index('article_id').reindex(similar_ids).reset_index()
    prod_data = matched_rows['prod_name'].values.tolist()
    grap_data = matched_rows['graphical_appearance_name'].values.tolist()
    return prod_data,grap_data

def carousel():
    df = pd.read_csv(serch_path)
    row_list = []
    for i in range(20):
        if len(row_list) < 12:
            random_num = random.randint(0,105542)
            if random_num not in row_list:
                row_list.append(random_num)
            else:
                continue
    match_rows = df.iloc[row_list]
    id = match_rows.article_id.values.tolist()
    
    return id