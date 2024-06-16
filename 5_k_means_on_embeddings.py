import pandas as pd
import ast
import numpy as np
from sklearn.cluster import KMeans

### Code related to the KMeans algorithm from "https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans"

df_total = pd.read_excel("emb_videos.xlsx")
df_total["k_50"] = False
df_total["k_100"] = False
df_total["k_500"] = False
df_total["k_1000"] = False

# keeping only rows that have embeddings
df_no_emb = df_total[df_total.embeddings == False]
df = df_total[df_total.embeddings != False]

df['embeddings'] = df['embeddings'].apply(lambda x: ast.literal_eval(x)) # needed to convert each embedding list back
embeddings = df['embeddings'].tolist()

# embedding vectors
embeddings = np.array(embeddings)

# number of clusters 
num_clusters = [50, 100, 500, 1000]

for clusters in num_clusters:
    # creating and fitting the KMeans model
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(embeddings)
    
    df[f'k_{clusters}'] = kmeans.labels_.astype(str) # saving the cluster labels

merged_df = pd.concat([df, df_no_emb])
merged_df.sort_index(inplace=True)

# saving the df
merged_df.to_excel('knn_videos.xlsx', index=False)