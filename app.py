from flask import Flask, render_template, redirect, jsonify
import pymongo
import scrape_mars

app = Flask("__name__")

mongo = pymongo.MongoClient("mongodb+srv://PrivateUser:dw765svWVsSWbsQavfhH@missiontomars.33wx7.mongodb.net/mars?retryWrites=true&w=majority", maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'mars')
col = pymongo.collection.Collection(db, 'mars_data')

@app.route("/")
def home():

    mars = col.find_one()
    return render_template("index.html", mars=mars)



# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    scrape_mars.scrape()

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
