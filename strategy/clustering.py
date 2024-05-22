from data_preparation import data
import matplotlib as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

data = data.drop('cluster', axis=1)

def get_clusters(data):
    data['cluster'] = KMeans(n_clusters=4,
                           random_state=0,
                           init=initial_centroids).fit(data).labels_
    return data

data = data.dropna().groupby('date', group_keys=False).apply(get_clusters)
def plot_clusters(data):

    cluster_0 = data[data['cluster']==0]
    cluster_1 = data[data['cluster']==1]
    cluster_2 = data[data['cluster']==2]
    cluster_3 = data[data['cluster']==3]

    plt.scatter(cluster_0.iloc[:,0] , cluster_0.iloc[:,6] , color = 'red', label='cluster 0')
    plt.scatter(cluster_1.iloc[:,0] , cluster_1.iloc[:,6] , color = 'green', label='cluster 1')
    plt.scatter(cluster_2.iloc[:,0] , cluster_2.iloc[:,6] , color = 'blue', label='cluster 2')
    plt.scatter(cluster_3.iloc[:,0] , cluster_3.iloc[:,6] , color = 'black', label='cluster 3')
    
    plt.legend()
    plt.show()
    return

plt.style.use('ggplot')
for i in data.index.get_level_values('date').unique().tolist():
    g = data.xs(i, level=0)
    plt.title(f'Date {i}')
    plot_clusters(g)

#define centroids
target_rsi_values = [30, 45, 55, 70]
initial_centroids = np.zeros((len(target_rsi_values), 18))
initial_centroids[:, 6] = target_rsi_values

filtered_data = data[data['cluster']==3].copy()
filtered_data = filtered_data.reset_index(level=1)
filtered_data.index = filtered_data.index+pd.DateOffset(1)
filtered_data = filtered_data.reset_index().set_index(['date', 'ticker'])
dates = filtered_data.index.get_level_values('date').unique().tolist()
fixed_dates = {}
for d in dates:
    fixed_dates[d.strftime('%Y-%m-%d')] = filtered_data.xs(d, level=0).index.tolist()
