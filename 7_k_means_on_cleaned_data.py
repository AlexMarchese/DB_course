import pandas as pd
import ast
import numpy as np
from sklearn.cluster import KMeans

### Code related to the KMeans algorithm from "https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans"

df_total = pd.read_excel("emb_videos.xlsx")
df_total["k_5"] = False
df_total["k_10"] = False
df_total["k_50"] = False
df_total["k_100"] = False

# keeping only rows that have embeddings
df_no_emb = df_total[df_total.embeddings == False]
df = df_total[df_total.embeddings != False]

df = df.groupby('company').filter(lambda x: len(x) >= 30) # taking only the companies with at least 30 videos
print(len(df['company'].unique())) # shows that 57 companies fulfill that condition

df = df.groupby('company').apply(lambda x: x.sample(n=30)).reset_index(drop=True) # taking a sample of 30 videos per company
print(df.shape) # 57 * 30 -> 1710 rows is correct


df['embeddings'] = df['embeddings'].apply(lambda x: ast.literal_eval(x)) # needed to convert each embedding list back
embeddings = df['embeddings'].tolist()

# embedding vectors
embeddings = np.array(embeddings)

# number of clusters 
num_clusters = [5, 10, 50, 100]

for clusters in num_clusters:
    # creating and fitting the KMeans model
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(embeddings)
    
    df[f'k_{clusters}'] = kmeans.labels_.astype(str) # saving the cluster labels

# saving the df
df.to_excel('knn_videos_cleaned_data.xlsx', index=False)