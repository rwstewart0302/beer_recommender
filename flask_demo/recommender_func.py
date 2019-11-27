import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances

df = pd.read_csv('../data/beer_reviews_col_drop.csv')
df.head()

# using a pivot table to create my recommender model
pivot = df.pivot_table(index='beer_name', columns='review_profilename',
                       values=['review_overall'])

pivot_sparse = sparse.csr_matrix(pivot.fillna(0))
recommender = pairwise_distances(pivot_sparse, metric='cosine')

recommender_df = pd.DataFrame(recommender, index=pivot.index, columns=pivot.index)


def brewery_recommender(user):
    # creating a list of the 20 most similar beers if the user rated these beers equal to or above 3.5 (0-5 scale)
    recs = []
    for key, value in user.items():
        rec = {}
        if value >= 3.5:
            rec[key] = recommender_df[key].sort_values()[1:11]
            recs.append(rec)

    beer_checklist = []

    for i in recs:
        # creating a list of beers to read back into the dataset to score breweries if the similarity score for that
        # beer is greater than or equal to 0.5
        for beer, scores in i.items():
            for recom, sim_scores in scores.items():
                #                 if sim_scores <= 0.5:
                beer_checklist.append((recom, sim_scores))

    # creating a list of breweries and the beer scores associated with that brewery to find the most
    # similar brewery based on the mean similarity score
    breweries = []
    current_beer = ''
    for beer in beer_checklist:
        for index, brewery in df[df['beer_name'] == beer[0]]['brewery_name'].items():
            if current_beer != beer[0]:
                current_beer = beer[0]
                brewery_score = (brewery, beer[1])
                breweries.append(brewery_score)

    # sorting the breweries alphabetically to make it easier to loop through
    current_brewery = ''
    scores = []
    brewery_dict = {}
    breweries_sort = sorted(breweries)
    for i in range(len(breweries_sort)):
        if breweries_sort[i][0] == current_brewery:
            scores.append(breweries_sort[i][1])
        else:
            if current_brewery:
                brewery_dict[current_brewery] = scores
            current_brewery = breweries_sort[i][0]
            scores = []
            scores.append(breweries_sort[i][1])
    return brewery_dict

# sorting the breweries mean similarity scores and counting the number of similar beers at that brewery
# similar beers are beers with similarity scores less than 0.5


def sorting_brewery_scores(users):
    best_breweries = {}
    for brewery, score in brewery_recommender(users).items():
        sim_beers = 0
        for i in score:
            if i < 0.5:
                sim_beers += 1

#         if 2 <= sim_beers:
        best_breweries[brewery] = (np.mean(score), 'number of similar beers: ', sim_beers)
#         else:
#             continue

    sorted_best_breweries = (sorted(best_breweries.items(), key=lambda kv: (kv[1], kv[0])))

    sorted_best_breweries = sorted_best_breweries[:3]

    if sorted_best_breweries[0][1][0] > 0.5:
        sorted_best_breweries = sorted_best_breweries[0][0]
    else:
        sorted_best_breweries = sorted_best_breweries

    return sorted_best_breweries
