from flask import Flask, render_template, redirect
# Module used to connect Python with MongoDb
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Default port used by mongodb is 27017
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
mongo = PyMongo(app)
# Define the mardDB database
#db = client.marsDB

@app.route("/")
def home():
    mars_data = mongo.db.marsDB.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
# Collection
    mars = mongo.db.marsDB
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert = True)
    return redirect("/", code=302)

# for data in db.mars.find():
#     print(type(data))

if __name__ == "__main__":
    app.run(debug=True)