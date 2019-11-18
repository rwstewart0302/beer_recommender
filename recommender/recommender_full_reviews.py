import pandas as pd
import sys
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

def main():
    beers_df = pd.read_csv('../../beer_reviews_full.csv')
    beers_df['review_time'] = pd.to_datetime( beers_df['review_time'], unit = 's' )
    beers_df = beers_df.loc[ beers_df[ 'review_time' ].dt.year >= 2002 ]
    pivot_mean = beers_df.pivot_table(index='beer_name', columns='review_profilename',
                       values=['review_overall'])

    pivot_mean_sparse = sparse.csr_matrix(pivot_mean.fillna(0))
    recommender_mean = pairwise_distances(pivot_mean_sparse, metric='cosine')
    recommender_df_mean = pd.DataFrame(recommender_mean, index=pivot_mean.index, columns=pivot_mean.index)
    return recommender_df_mean.to_csv("recommender_file.csv", index=False)
main()
