# Dependencies
from flask import Flask, render_template, redirect
# Module used to connect Python with MongoDb
import pymongo
from flask_pymongo import PyMongo
# Import the python file used for web scrapping
import scrape_mars

app = Flask(__name__)

# Default port used by mongodb is 27017
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
mongo = PyMongo(app)
# Create a route that will query Mongo database and sends initial dict values of mars database into an HTML template to display the data.
@app.route("/")
def home():
    mars_data = mongo.db.marsDB.find_one()
    return render_template("index.html", mars_data=mars_data)

# Create a route that displays all of the information that was scraped in scrape.py file
@app.route("/scrape")
def scraper():
# Collection
    mars = mongo.db.marsDB
    # Write the scraped data in database
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert = True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)