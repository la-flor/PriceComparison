from models import db, connect_db, Activity, Product, Category, ListingAssociation, VendorListing
from app import tokens
import requests
from app import app
import os

app.config['API_KEY'] = os.environ.get('API_KEY')

db.drop_all()
db.create_all()


act1 = Activity(activity="Climbing", image="static/images/activity_climb.jpeg")
act2 = Activity(activity="Trail Running", image="static/images/activity_run.jpeg")
act3 = Activity(activity="Camping", image="static/images/activity_camp.jpeg")
db.session.add_all([act1,act2,act3])
db.session.commit()

cat1 = Category(category_name="Belay Devices", activity=act1)

cat4 = Category(category_name="Chalk", activity=act1)
cat5 = Category(category_name="Carabiners", activity=act1)

cat7 = Category(category_name="Mens Trail Shoes", activity=act2)
cat8 = Category(category_name="Womens Trail Shoes", activity=act2)

cat12 = Category(category_name="Sleeping Bags", activity=act3)
cat13 = Category(category_name="Sleeping Pads", activity=act3)

db.session.add_all([cat1,cat4,cat5,cat7,cat8,cat12,cat13])
db.session.commit()

# To add in the future:

# Activities:
# act4 = Activity(activity="Skiing", image="static/images/activity_ski.jpeg")

# Categories:
# cat2 = Category(category_name="Male Climbing Harness", activity=act1)
# cat3 = Category(category_name="Female Climbing Harness", activity=act1)
# cat6 = Category(category_name="Quickdraws", activity=act1)
# cat9 = Category(category_name="Running Packs", activity=act2)
# cat10 = Category(category_name="Backpacks", activity=act3)
# cat11 = Category(category_name="Tents", activity=act3)

errors = []

for retailer in ["Backcountry", "REI"]:
    token = tokens[retailer]
    resp = requests.get(f'https://www.parsehub.com/api/v2/projects/{token}/last_ready_run/data', params={"api_key": API_KEY})
    data = resp.json()
    product_errors = []
    for cat in data[retailer]:
        for product in cat["products"]:
            if product and Product.query.filter_by(model=product["model"]).first():
                # If product is already found in Products table, do not create a new product.
                # Only create a new vendor_listing and listing_association entry.
                try:
                    v_listing = VendorListing(vendor_name=retailer,
                                                    model_url=product["model_url"],
                                                    price=product["price"])
                    db.session.add(v_listing)
                    db.session.commit()

                    listing_relationship = ListingAssociation(product_id=Product.query.filter_by(model=product["model"]).first().id,
                                                                vendor_id=v_listing.id)
                    db.session.add(listing_relationship)
                    db.session.commit()
                except:
                    product_errors.append(product)

            elif product:
                # If this product is not already in the products table, create new entry in products table
                # and create a vendor_listing and listing_association entry.
                try:
                    category_id = Category.query.filter_by(category_name=cat["category"]).first()
                    prod = Product(brand=product["brand"],
                                    model=product["model"],
                                    image=product["image"],
                                    category=category_id)
                    db.session.add(prod)
                    db.session.commit()

                    v_listing = VendorListing(vendor_name=retailer,
                                                    model_url=product["model_url"],
                                                    price=product["price"])
                    db.session.add(v_listing)
                    db.session.commit()

                    listing_relationship = ListingAssociation(product_id=Product.query.filter_by(model=product["model"]).first().id,
                                                                vendor_id=v_listing.id)
                    db.session.add(listing_relationship)
                    db.session.commit()
                except:
                    product_errors.append(product)
    
print(product_errors)