from models import Activity, Product, Category, Company, db
from app import app

db.drop_all()
db.create_all()


act1 = Activity(activity="Climbing", image="static/images/activity_climb.jpeg")
act2 = Activity(activity="Trail Running", image="static/images/activity_run.jpeg")
act3 = Activity(activity="Camping", image="static/images/activity_camp.jpeg")
act4 = Activity(activity="Skiing", image="static/images/activity_ski.jpeg")
db.session.add_all([act1,act2,act3,act4])
db.session.commit()

cat1 = Category(category_name="Belay Devices", activity=act1)
cat2 = Category(category_name="Mens Climbing Harness", activity=act1)
cat3 = Category(category_name="Womens Climbing Harness", activity=act1)
cat4 = Category(category_name="Chalk", activity=act1)
cat5 = Category(category_name="Carabiners", activity=act1)
cat6 = Category(category_name="Quickdraws", activity=act1)
cat7 = Category(category_name="Mens Trail Shoes", activity=act2)
cat8 = Category(category_name="Womens Trail Shoes", activity=act2)
db.session.add_all([cat1,cat2,cat3,cat4,cat5,cat6,cat7,cat8])
db.session.commit()

comp1 = Company(company_name="Backcountry")
comp2 = Company(company_name="REI")
db.session.add_all([comp1,comp2])
db.session.commit()

