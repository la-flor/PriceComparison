from flask import Flask, render_template, redirect, flash
import requests
from keys import API_KEY, SECRET_KEY, tokens
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Activity, Product, Category, Company
# from seed import seed_db
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///price_comparison'

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return render_template('home.html')

def seed_db(retailer, data):
    company_id = Company.query.filter_by(company_name=retailer).first()
    for cat in data[retailer]:
        for product in cat["products"]:
            category_id = Category.query.filter_by(category_name=cat["category"]).first()
            prod = Product(brand=product["brand"],
                            model=product["model"],
                            model_url=product["model_url"],
                            image=product["image"],
                            price=product["price"],
                            company=company_id,
                            category=category_id)
            db.session.add(prod)
            db.session.commit()

@app.route('/upload')
def import_data():
    for retailer in ["Backcountry", "REI"]:
        token = tokens[retailer]
        resp = requests.get(f'https://www.parsehub.com/api/v2/projects/{token}/last_ready_run/data', params={"api_key": API_KEY})
        data = resp.json()
        seed_db(retailer, data)
    return redirect('/')

@app.route('/retailers')
def retailers():
    return render_template('retailers.html')

@app.route('/retailers/<retailer>')
def show_by_retailer(retailer):
    if retailer not in tokens:
        flash("Invalid retailer request")
        return redirect('/retailers')
    
    token = tokens[retailer]
    resp = requests.get(f'https://www.parsehub.com/api/v2/projects/{token}/last_ready_run/data', params={"api_key": API_KEY})
    data = resp.json()
    return render_template('retailer.html', retailer=retailer, products=data[retailer])

@app.route('/activities')
def activities():
    activities = Activity.query.all()
    return render_template('activities.html', activities=activities)


@app.route('/activity/<activity>')
def activity_products(activity):
    activity_id = Activity.query.filter_by(activity=activity).first().id
    categories = Category.query.filter_by(activity_id=activity_id).all()

    return render_template('activity_categories.html', activity=activity, categories=categories)

@app.route('/activity/<activity>/<category>')
def category_products(activity, category):
    cat = Category.query.filter_by(category_name=category).first()
    products = Product.query.filter_by(category_id=cat.id).all()
    # pdb.set_trace()
    return render_template('category_products.html', category=category, activity=activity, products=products)


# @app.route('/activity/<activity>')
# def activity_products(activity):
#     activity = activity.lower()
#     products = {}
#     set_products = set()

#     categories = {"climb": ["belay_devices"], "hike_and_camp": [], "run": ["mens_trail_running_shoes"], "ski": [], "paddle": [], "fish": []}

#     for retailer in tokens:
#         for subcategory in categories[activity]:
#             token = tokens[retailer]
#             resp = requests.get(f'https://www.parsehub.com/api/v2/projects/{token}/last_ready_run/data', params={"api_key": API_KEY})
#             data = resp.json()
#             for index in data[retailer]:
#                 if index["category"]:
#                     products[retailer] = index["products"]
#                     [set_products.add(item['model']) for item in index["products"]]

#     return render_template('activity_products.html', activity= activity, set_products=set_products, products=products)