from flask import Flask, render_template, redirect, flash, request, jsonify
import requests
import json
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Activity, Product, Category, ListingAssociation, VendorListing
import pdb
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///price_comparison')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['API_KEY'] = os.environ.get('PRICE_COMP_API_KEY')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# toolbar = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/activities')
def activities():
    """ Show activity options - ex: climbing, trail running """
    activities = Activity.query.all()
    return render_template('activities.html', activities=activities)

@app.route('/activity/<activity>', methods=["GET", "POST"])
def products(activity):
    """ Display products for selected activity with the ability to filter products """

    activity_id = Activity.query.filter_by(activity=activity).first().id
    all_categories = Category.query.filter_by(activity_id=activity_id).all()
    cat_ids = []
    banners = {"Trail Running": "banner_trailrun.png", "Camping": "banner_camping.png", "Climbing": "banner_climbing.png"}
    
    banner = banners[activity]

    for cat in all_categories:
        cat_ids.append(cat.id)

    if request.method == "POST":
        params = request.form["search"]
        products = []
        models = Product.query.filter(Product.model.ilike(f'%{params}%')).all()
        make = Product.query.filter(Product.brand.ilike(f'%{params}%')).all()
        
        if models:
            for prod in models:
                if prod.category_id in cat_ids:
                    products.append(prod)
        if make:
            for prod in make:
                if prod.category_id in cat_ids:
                    products.append(prod)

        return render_template('products.html', categories=all_categories, activity=activity, products=products, banner=banner)

    elif request.args:
        filters = []
        
        """Identify visitor filter selection to apply and add to filters list"""
        for option in all_categories:
            if option.category_name in request.args:
                filters.append(option.category_name)
        
        """Get the category id of the filters to be applied"""
        filter_ids = []
        for cat in filters:
            category = Category.query.filter_by(category_name=cat).first()
            filter_ids.append(category.id)
        
        """Identify products in filtered categories and add to products list"""
        products = []
        for identity in filter_ids:
            filtered_products = Product.query.filter_by(category_id=identity).all()
            for product in filtered_products:
                products.append(product)
        return render_template('products.html', checked=filters, categories=all_categories, activity=activity, products=products, banner=banner)

    else:
        category = Category.query.filter_by(activity_id=activity_id).all()
        products = []
        for cat in category:
            cat_prods = Product.query.filter_by(category_id=cat.id).all()
            for prod in cat_prods:
                products.append(prod)

        return render_template('products.html', categories=all_categories, activity=activity, products=products, banner=banner)