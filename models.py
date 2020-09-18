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
    model_url = db.Column(db.Text,
                        nullable=False)
    image = db.Column(db.Text,
                        nullable=False)
    price = db.Column(db.Float,
                        nullable=False)
    company_id = db.Column(db.Integer,
                        db.ForeignKey("companies.id"))
    category_id = db.Column(db.Integer,
                        db.ForeignKey("categories.id"))


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
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))
    products = db.relationship("Product", backref="category")

class Company(db.Model):
    """Company identification"""
    __tablename__ = "companies"

    id = db.Column(db.Integer,
                        primary_key=True)
    company_name = db.Column(db.Text,
                                nullable=False,
                                unique=True)
    products = db.relationship("Product", backref="company")

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)