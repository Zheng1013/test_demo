import pandas as pd
import numpy as np
from pathlib import Path

parquet_path = Path(__file__).resolve().parent / 'test2_2.parquet'

#輸入年紀調用的function 

def age(age_input):
    df = pd.read_parquet(parquet_path)
    # age = int(input("Choose Your Age:"))
    age = age_input
        # 年紀上下限
    top_limit, bottom_limit = age + 5, age - 5
        # 年紀篩選
    age_df = df[(df['age'] <= top_limit) & (df['age'] >= bottom_limit)]
    
    # index_group_name
    index_group_name_list = age_df['index_group_name'].unique().tolist()
    return index_group_name_list , age_df

#輸入年紀後,選擇的product_index調用的function 

def product_index(input_product_index,age_df):
    product_index = input_product_index
    selected_df = age_df

    index_df = selected_df.groupby('index_group_name').get_group(product_index)

    # product_group_name
    product_group_name_list = index_df['product_group_name'].unique().tolist()
    return product_group_name_list , index_df

# 根據選擇的product_group調用的function

def product_group(intput_product_group,index_df):
    product_group = intput_product_group
    selected_df = index_df 

    if product_group != '':
        selected_df = selected_df.groupby('product_group_name').get_group(product_group)
    else:
        pass

    # product_group_type
    product_group_type_list = selected_df['product_type_name'].unique().tolist()
    return product_group_type_list , selected_df