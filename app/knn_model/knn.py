import pandas as pd
import scipy.sparse
from sklearn.neighbors import NearestNeighbors
from pathlib import Path

npz_path = Path(__file__).resolve().parent / 'sparse_matrix.npz'
df_path = Path(__file__).resolve().parent / 'encode_articles.csv'

def knn_model(i):
    sparse_matrix = scipy.sparse.load_npz(npz_path)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    encode_articles = pd.read_csv(df_path)
    encode_articles = encode_articles.article_id.to_list()
    model_knn.fit(sparse_matrix)
    
    i = encode_articles.index(i)
    x = sparse_matrix[i,:].toarray().reshape(1,-1)
    CF = model_knn.kneighbors(x, 6,return_distance=False)
    
    Recommender_item = []
    for ii in CF[0]:
        # if ii != i:
        #     item=encode_articles[ii]
        #     Recommender_item.append(item)
        item=encode_articles[ii]
        Recommender_item.append(item)
    
    
    return Recommender_item
