import pandas as pd
import ast
import numpy as np
from sklearn.cluster import KMeans

df = pd.read_excel("knn_videos.xlsx")

df = df[df.embeddings != False] # keeping the entries where embeddings exist

average_views_per_company = df.groupby('company')['views'].mean()

df['average_views'] = (df['company'].map(average_views_per_company))
df['relat_to_avg'] = (df['views'] / df['average_views']).round(4)

df['average_views'] = df['average_views'].round().astype(int)


df.to_excel('knn_videos_normalized.xlsx', index=False)