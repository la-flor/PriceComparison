from app import app
from unittest import TestCase
from models import db, Activity, Product, Category, ListingAssociation, VendorListing

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pricecomp_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

class FlaskAppTestCase(TestCase):
    """Test for route requests"""

    def setUp(self):
        """Clear all data and setup database for database info to be tested on html pages"""
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

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_home_page(self):
        """Test home page request returns home.html successfully"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="carouselSlides"', html)
    
    def test_retailers(self):
        """Test retailers page request returns retailers.html successfully"""
        with app.test_client() as client:
            resp = client.get('/retailers')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 id="title-retailers">Current Retailers</h1>', html)
    
    def test_activities(self):
        """Test activities page request returns activities.html and includes activities on page"""
        with app.test_client() as client:
            resp = client.get('/activities')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 id="title-activities">Activities</h1>', html)
            self.assertIn("Climbing", html)
    
    def test_products(self):
        """Test products page request returns products.html and includes products on page"""
        with app.test_client() as client:
            resp = client.get('/activity/Climbing')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Climbing", html)
            self.assertIn("Filters", html)
            self.assertIn("Belay Devices", html)
            self.assertIn("ATC Belay Device", html)