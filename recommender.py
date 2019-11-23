# importing libraries
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances

import numpy as np
import requests

from flask import Flask, render_template, url_for, request

app = Flask(__name__)


df = pd.read_csv('data/beer_reviews_col_drop.csv')

# using a pivot table to create my recommender model
pivot = df.pivot_table(index='beer_name', columns='review_profilename',
                       values=['review_overall'])

pivot_sparse = sparse.csr_matrix(pivot.fillna(0))
recommender = pairwise_distances(pivot_sparse, metric='cosine')
recommender_df = pd.DataFrame(recommender, index=pivot.index, columns=pivot.index)

# clearing everything I don't need for the model to save memory
pivot = []
recommender = []
pivot_sparse = []


@app.route("/")
def hello():
    return render_template('echo.html')


@app.route("/echo", methods=['POST'])
def echo():
    return render_template('echo.html')


if __name__ == "__main__":
    app.run(debug=True)
