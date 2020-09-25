from unittest import TestCase

from app import app
from models import db, Activity, Product, Category, ListingAssociation, VendorListing

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pricecomp_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

class SeedDatabaseTestCase(TestCase):
    """Test for adding products to database"""

    def setUp(self):
        """Clear all data and create database information"""
        db.drop_all()
        db.create_all()

        act1 = Activity(activity="Climbing", image="static/images/activity_climb.jpeg")
        act1.id = 1111

        cat1 = Category(category_name="Belay Devices", activity=act1)
        cat1.id = 2222

        prod1 = Product(brand="Black Diamond", model="ATC Belay Device", image="image.jpg", category_id=2222)
        prod1.id = 3333

        db.session.add_all([act1, cat1, prod1])
        db.session.commit()

        list1 = VendorListing(vendor_name="REI", model_url="product_source.com", price=19.99)
        list1.id = 4444

        db.session.add(list1)
        db.session.commit()

        assos1 = ListingAssociation(product_id=3333, vendor_id=4444)
        assos1.id = 5555

        db.session.add(assos1)
        db.session.commit()

        self.act1 = Activity.query.get(act1.id)
        self.cat1 = Category.query.get(cat1.id)
        self.prod1 = Product.query.get(prod1.id)
        self.list1 = VendorListing.query.get(list1.id)
        self.assos1 = ListingAssociation.query.get(assos1.id)


    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
    
    def test_activities(self):
        """Test activities model"""
        
        self.assertEqual(self.act1.activity, "Climbing")
        self.assertEqual(self.act1.image, "static/images/activity_climb.jpeg")
    
    def test_categories(self):
        """Test categories model"""

        self.assertEqual(self.cat1.category_name, "Belay Devices")
        self.assertEqual(self.cat1.activity, self.act1)
    
    def test_products(self):
        """Test products model"""
        
        self.assertEqual(self.prod1.brand, "Black Diamond")
        self.assertEqual(self.prod1.model, "ATC Belay Device")
        self.assertEqual(self.prod1.image, "image.jpg")
        self.assertEqual(self.prod1.category_id, self.cat1.id)
    
    def test_vendor_listing(self):
        """Test vendor_listings model"""

        self.assertEqual(self.list1.vendor_name, "REI")
        self.assertEqual(self.list1.model_url, "product_source.com")
        self.assertEqual(self.list1.price, 19.99)

    def test_listing_associations(self):
        """Test listing_associations model"""

        self.assertEqual(self.assos1.product_id, self.prod1.id)
        self.assertEqual(self.assos1.vendor_id, self.list1.id)