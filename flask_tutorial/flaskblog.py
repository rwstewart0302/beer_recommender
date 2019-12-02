from flask import Flask, render_template, url_for, flash, redirect, request
from forms import BeerRatings, LoginForm
from flask_caching import Cache
from recommender_func import data_manipulation
app = Flask(__name__)
cache = Cache()

app.config['SECRET_KEY'] = '9d63ec1e4d5d77e21472d78203e949bb'

main_page_content = [
    # {
    #     'content': 'Login Here to Get Your Brewery Recommendation!',
    #     'hypertext': 'Login',
    #     'link': '/login'
    # },
    # {
    #     'content': 'If you Don\'t Have an Account Create One Here!',
    #     'hypertext': 'Register',
    #     'link': '/beer_ratings'
    # },
    {
        'content': 'Rate Beers To Get Your Brewery Recommendation!',
        'hypertext': 'Click Here!',
        'link': '/beer_ratings'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=main_page_content)


@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/beer_ratings')
def ratings():
    return render_template('ratings.html')


@app.route('/recommendations')
def recommendations():
    rating = request.args
    ratings = {'90 Minute IPA': float(rating['90MinuteIPA']),
               'Old Rasputin Russian Imperial Stout': float(rating['OldRasp']),
               'Sierra Nevada Celebration Ale': float(rating['SNCeleb']),
               'Two Hearted Ale': float(rating['TwoHeart']),
               'Stone Ruination IPA': float(rating['StoneRuin']),
               'Arrogant Bastard Ale': float(rating['ArrgB']),
               'Sierra Nevada Pale Ale': float(rating['SNPale']),
               'Stone IPA (India Pale Ale)': float(rating['StoneIPA']),
               'Pliny The Elder': float(rating['Pliny']),
               'Founders Breakfast Stout': float(rating['FoundBreak'])
               }
    recommendations = data_manipulation(ratings)
    beers = recommendations[1]
    return render_template('recommendations.html', recommendations=beers)
    # return render_template('recommendations.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
