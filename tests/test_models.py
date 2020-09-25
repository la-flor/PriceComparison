from unittest import TestCase

from app import app
from models import db, Activity, Product, Category, ListingAssociation, VendorListing

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pricecomp_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class SeedDatabaseTestCase(TestCase):
    """Test for adding products to database"""

    def setUp(self):
        """Clear all data"""

    
    def tearDown(self):
        