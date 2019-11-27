from flask import Flask, render_template, url_for, flash, redirect, request
from forms import BeerRatings, LoginForm
from flask_caching import Cache
from recommender_func import sorting_brewery_scores
app = Flask(__name__)
cache = Cache()

app.config['SECRET_KEY'] = '9d63ec1e4d5d77e21472d78203e949bb'

main_page_content = [
    {
        'content': 'Login Here to Get Your Brewery Recommendation!',
        'hypertext': 'Login',
        'link': '/login'
    },
    {
        'content': 'If you Don\'t Have an Account Create One Here!',
        'hypertext': 'Register',
        'link': '/beer_ratings'
    },
    {
        'content': 'Don\'t Want to Create an Account? No Problem! Get Beer Recommendation Here',
        'hypertext': 'Register',
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


@app.route('/beer_ratings', methods=["GET", "POST"])
def ratings():
    form = BeerRatings()
    if form.validate_on_submit():
        # flash(f'Account created for {form.dog_rating.data}!', 'success')
        ratings = {'90 Minute IPA': form.dogfish_head_rating.data,
                   'Old Rasputin Russian Imperial Stout': form.old_ras_rating.data,
                   'Sierra Nevada Celebration Ale': form.sn_cel_rating.data,
                   'Two Hearted Ale': form.two_heart_rating.data,
                   'Stone Ruination IPA': form.stone_ruin_rating.data,
                   'Arrogant Bastard Ale': form.arr_bast_rating.data,
                   'Sierra Nevada Pale Ale': form.sn_pale_rating.data,
                   'Stone IPA (India Pale Ale)': form.stone_ipa_rating.data,
                   'Pliny The Elder': form.pliny_rating.data,
                   'Founders Breakfast Stout': form.founders_rating.data
                   }
        # return str(form.dogfish_head_rating.data)
        recommendation = str(sorting_brewery_scores(ratings))
        return redirect(url_for('recommendations', recommendation=recommendation))
        # return render_template('ratings.html',  recommendation=recommendation)

    return render_template('ratings.html', title='Register', form=form)


@app.route('/recommendations', methods=["GET", "POST"])
def recommendations():
    recommendation = request.args
    return render_template('recommendations.html', recommendation=recommendation)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
