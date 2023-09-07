import pandas as pd
import numpy as np
from pathlib import Path

parquet_path = Path(__file__).resolve().parent / 'firstInput.parquet'

#輸入年紀調用的function 

def get_index(age_input):
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

def get_group_list(input_product_index,age_df):
    product_index = input_product_index
    selected_df = age_df

    index_df = selected_df.groupby('index_group_name').get_group(product_index)

    # product_group_name
    product_group_name_list = index_df['product_group_name'].unique().tolist()
    return product_group_name_list , index_df

# 根據選擇的product_group調用的function

def get_type_list(intput_product_group,index_df):
    product_group = intput_product_group
    selected_df = index_df 

    if product_group != 'None':
        selected_df = selected_df.groupby('product_group_name').get_group(product_group)
    else:
        pass

    # product_group_type
    product_group_type_list = selected_df['product_type_name'].unique().tolist()
    return product_group_type_list , selected_df

def get_article(input_type,userInput_color,selected_df):
    product_type = input_type
    if product_type != '':
        selected_df = selected_df.groupby('product_type_name').get_group(product_type)
    else:
        pass

    # 顏色（選填）(Optional)Choose Colors:("space" for different colors, "_" for describing color)'
    color_inputing = userInput_color
    if color_inputing != '':
        color_input = []

        for i in color_inputing.split(' '):
            i = i.lower()
            i = i.replace('_', ' ')
            color_input.append(i)

        sdf_colors = np.array(selected_df['colour_group_name'].str.lower().unique().tolist())
        same_colors = []
        for i in color_input:
            same_color = sdf_colors[sdf_colors == i]
            try:
                same_colors.append(same_color[0])
            except:
                pass

        if selected_df[selected_df['colour_group_name'].str.lower().isin(same_colors)].shape[0] == 0:
            pass
            #display(selected_df)
        else:
            selected_df = selected_df[selected_df['colour_group_name'].str.lower().isin(same_colors)]
            #display(selected_df)

    # 商品銷售排序&展現
    selected_df['product_full'] = selected_df['article_id'].astype(str) + '_' + selected_df['product_type_name'] + '_' + selected_df['prod_name'] + '_' + selected_df['colour_group_name'] 
    top10 = dict(selected_df['product_full'].value_counts(sort=True).head(10))
    top10 = pd.DataFrame({'Product':top10.keys(), 'Sales Volume': top10.values()}, index = range(1,len(top10)+1))
    top10['article_id'] = top10['Product'].str.split('_').str[0].astype(str)
    top10['Product Type'] = top10['Product'].str.split('_').str[1]
    top10['Product Name'] = top10['Product'].str.split('_').str[2]
    top10['Color'] = top10['Product'].str.split('_').str[-1]
    top10.drop(columns = ['Product'], inplace = True)
    top10 = top10[['article_id', 'Product Name', 'Color', 'Product Type', 'Sales Volume']]
    return top10

