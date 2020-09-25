"""Models for Price Comparison web app"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    """Define products and link to categories and companies"""
    __tablename__ = "products"

    id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    brand = db.Column(db.Text,
                        nullable=False)
    model = db.Column(db.Text,
                        nullable=False)
    image = db.Column(db.Text,
                        nullable=False)
    category_id = db.Column(db.Integer,
                        db.ForeignKey("categories.id"))
    activity = db.relationship("Activity",
                                secondary="categories",
                                backref="products")
    listings = db.relationship("VendorListing",
                                secondary="listing_associations",
                                backref="products")


class Activity(db.Model):
    """Defined activities and picture for reference"""
    __tablename__ = "activities"
    
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.Text,
                            nullable=False,
                            unique=True)
    image = db.Column(db.Text)
    category = db.relationship("Category", backref="activity")

class Category(db.Model):
    """Category identification"""
    __tablename__ = "categories"

    id = db.Column(db.Integer,
                        primary_key=True)
    category_name = db.Column(db.Text,
                                nullable=False,
                                unique=True)
    image = db.Column(db.Text)
    # need to make image nullable = false after retrieving relevant images
    activity_id = db.Column(db.Integer,
                                db.ForeignKey("activities.id"))
    products = db.relationship("Product",
                                backref="category")

class ListingAssociation(db.Model):
    """Links relationship between vendors and the products that they sell that have been scraped"""
    __tablename__ = "listing_associations"

    id = db.Column(db.Integer,
                        primary_key=True)
    product_id = db.Column(db.Integer,
                            db.ForeignKey("products.id"))
    vendor_id = db.Column(db.Integer,
                            db.ForeignKey("vendor_listings.id"))

class VendorListing(db.Model):
    """Vendor/Company identification for sourced products"""
    __tablename__ = "vendor_listings"

    id = db.Column(db.Integer,
                        primary_key=True)
    vendor_name = db.Column(db.Text,
                                nullable=False)
    model_url = db.Column(db.Text,
                        nullable=False)
    price = db.Column(db.Float,
                        nullable=False)


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)