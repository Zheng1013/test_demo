import pandas as pd
import numpy as np
from pathlib import Path

parquet_path = Path(__file__).resolve().parent / 'test2_2.parquet'

def age(age_input):
    df = pd.read_parquet(parquet_path)
    # age = int(input("Choose Your Age:"))
    age = age_input
        # 年紀上下限
    top_limit, bottom_limit = age + 5, age - 5
        # 年紀篩選
    selected_df = df[(df['age'] <= top_limit) & (df['age'] >= bottom_limit)]
    
    # index_group_name
    index_group_name_list = selected_df['index_group_name'].unique().tolist()
    return index_group_name_list

