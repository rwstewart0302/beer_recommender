import pandas as pd
import numpy as np
# from scipy import sparse

# loading in the beer and brewery dataframe and the recommender demo dataframe
df = pd.read_csv('../new_capstone_repo/beer_recommender/data/beer_reviews_col_drop.csv')
recommender_df = pd.read_csv('../new_capstone_repo/beer_recommender/data/recommender_demo.csv')
recommender_df.set_index('beer_name', inplace=True)


def brewery_recommender(user):
    # creating a list of the 20 most similar beers if the user rated these beers equal to or above 3.5 (0-5 scale)
    recs = []
    rating_scale = []

    for key, value in user.items():
        rec = {}
        if value >= 3.5:
            rec[key] = recommender_df[key].sort_values()[1:11]
            recs.append(rec)
            rating_scale.append(value)

    count = 0
    scaler_count = 0
    scaler = rating_scale[scaler_count]
    beer_checklist = []

    for i in recs:
        for beer, scores in i.items():
            for recom, score in scores.items():
                count += 1
                if count % 11 == 0:
                    scaler_count += 1
                    try:
                        scaler = rating_scale[scaler_count]
                    except:
                        continue
                scaled_value = 1 + ((scaler - 3.5) / scaler)
                beer_checklist.append((recom, score / scaled_value))

    # creating a list of breweries and the beer scores associated with that brewery to find the most
    # similar brewery based on the mean similarity score
    breweries = []
    current_beer = ''
    for beer in beer_checklist:
        for index, brewery in df[df['beer_name'] == beer[0]]['brewery_name'].items():
            if current_beer != beer[0]:
                current_beer = beer[0]
                brewery_score = (brewery, beer[1], beer[0])
                breweries.append(brewery_score)

    # sorting the breweries alphabetically to make it easier to loop through
    current_brewery = ''
    scores = []
    brewery_dict = {}
    beer_dict = {}
    beers_dict = {}
    breweries_sort = sorted(breweries)
    for i in range(len(breweries_sort)):
        if breweries_sort[i][0] == current_brewery:
            current_beer = breweries_sort[i][2]
            beer_dict[current_beer] = breweries_sort[i][1]
            scores.append(breweries_sort[i][1])
        else:
            if current_brewery:
                brewery_dict[current_brewery] = scores
                beers_dict[current_brewery] = beer_dict
                beer_dict = {}
            current_brewery = breweries_sort[i][0]
            current_beer = breweries_sort[i][2]

            beer_dict[current_beer] = breweries_sort[i][1]
            scores = []
            scores.append(breweries_sort[i][1])
    return beers_dict


def sorting_brewery_scores(rand_user):
    brewery_score = {}
    scores = []
    for brewery, beer_scores in brewery_recommender(rand_user).items():
        scores_brew = []
        brewery_score[brewery] = scores_brew
        for beer, score in beer_scores.items():
            scores_brew.append(score)
        scores.append(scores_brew)

    sim_beers_all = []
    breweries = []
    scores = []
    best_breweries = {}
    best_breweries_beers = {}

    for brewery, beer_scores in brewery_recommender(rand_user).items():
        beers = []
        for beer, score in beer_scores.items():
            if score < 0.5:
                beers.append(beer)
        best_breweries_beers[brewery] = beers

    for brewery, score in brewery_score.items():
        sim_beers = 0
        for j in score:
            if j < 0.5:
                sim_beers += 1
        breweries.append(brewery)
        sim_beers_all.append(sim_beers)
        scores.append(np.mean(score))

    best_breweries['brewery'] = breweries
    best_breweries['similar_beers'] = sim_beers_all
    best_breweries['score'] = scores

    return best_breweries, best_breweries_beers


def data_manipulation(rand_user):
    recs = sorting_brewery_scores(rand_user)
    best_beers = recs[1]
    data = pd.DataFrame(recs[0])
    # data.set_index('brewery', inplace=True)
    new_recs = data.sort_values(['score']).loc[(data.sort_values(['score'])['similar_beers'] >= 1) &
                                               (data.sort_values(['score'])['score'] < 0.5)]

    beers = {}
    for i in new_recs['brewery']:
        beer_list = []
        check = 1
        for brewery, beer in best_beers.items():
            if i == brewery and len(beer) > 0:
                beer_list = beer
                check = 0
        if check == 0:
            beers[i] = beer_list

    return new_recs, beers
