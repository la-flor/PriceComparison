from flask import Flask, render_template, redirect, flash, request, jsonify
import requests
import json
from keys import API_KEY, SECRET_KEY, tokens
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Activity, Product, Category, ListingAssociation, VendorListing
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

@app.route('/retailers')
def retailers():
    return render_template('retailers.html')

@app.route('/activities')
def activities():
    """ Show activity options - ex: climbing, trail running """
    activities = Activity.query.all()
    return render_template('activities.html', activities=activities)

@app.route('/activity/<activity>', methods=["GET"])
def products(activity):
    """ Display products for selected activity with the ability to filter products """

    activity_id = Activity.query.filter_by(activity=activity).first().id
    all_categories = Category.query.filter_by(activity_id=activity_id).all()

    if request.args:
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
        return render_template('products.html', checked=filters, categories=all_categories, activity=activity, products=products)

    category = Category.query.filter_by(activity_id=activity_id).all()
    products = []
    for cat in category:
        cat_prods = Product.query.filter_by(category_id=cat.id).all()
        for prod in cat_prods:
            products.append(prod)

    return render_template('products.html', categories=all_categories, activity=activity, products=products)