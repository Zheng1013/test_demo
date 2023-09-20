#import packaged
import pandas as pd
import numpy as np
import scipy.sparse
from sklearn.neighbors import NearestNeighbors
from pathlib import Path

npz_path = Path(__file__).resolve().parent / 'user_sparse_matrix.npz'

def knn_model(item_ids):
    #load data
    sparse_matrix = scipy.sparse.load_npz(npz_path)
    model_knn = NearestNeighbors(metric = 'cosine')
    df=pd.read_parquet('D:\\BDSE31_Team5\\workplace\\eachCusBoughtdata\\each_customer_bough.parquet')
    df_encodearticle = pd.read_parquet('D:\\BDSE31_Team5\\workplace\\eachCusBoughtdata\\encode_articles.parquet')
    encodearticle = df_encodearticle.article_id.to_list()
    
    #boughtList encode
    # EC_boughtList = []
    # boughtList=boughtList[-5:]
    # for i in boughtList:
    #     tmp = encodearticle.index(i)
    #     EC_boughtList.append(tmp)

    EC_item_ids = []
    for item_id in item_ids:
        tmp = encodearticle.index(item_id)
        EC_item_ids.append(tmp)


    #build KNN model
    model_knn = NearestNeighbors(metric = 'cosine')
    model_knn.fit(sparse_matrix)

    #EncodeList to InputArray
    # bought_array = np.zeros((1, 105542))
    # for i in EC_boughtList:
    #     bought_array[0, i] = 1
    
    item_array = np.zeros((1, 105542))
    for i in EC_item_ids:
        item_array[0, i] = 1


    #Run knn
    # CF = model_knn.kneighbors(bought_array, 10,return_distance=False)
    # CF = CF[0][:]
    # CF=CF.tolist()

    CF = model_knn.kneighbors(item_array, 10, return_distance=False)
    CF = CF[0][:]
    CF = CF.tolist()

    #
    recommandation = set()
    for i in CF:
        temp = df.loc[df['encode_customer_id'] == i]['encode_article_id'].to_list()[0].split(',')
        temp = set(map(int, temp))
        recommandation = (recommandation | temp)

    recommandlist =[]
    for i in recommandation:
        recommandlist.append(encodearticle[i])
        
    if len(recommandlist)>5:
        recommandlist = recommandlist[:5]
        return recommandlist
    else:
        return recommandlist
