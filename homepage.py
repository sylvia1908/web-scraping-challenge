from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)
# Mars ={}

mongo = PyMongo(app, uri="mongodb://localhost:27017/MarsMission")

@app.route("/")
def index():
    # blank ={"factTable":""}
    Mars = mongo.db.Mars.find_one()
    return render_template("index.html",Mars=Mars)
    
@app.route("/scrape")
def scraper():
    Mars = mongo.db.Mars
    Mars_data = scrape_mars.scrape()
    Mars.update({}, Mars_data, upsert=True)
    return redirect("/", code=302)


    # return redirect("/").
    

if __name__ == "__main__":
    app.run(debug=True)
