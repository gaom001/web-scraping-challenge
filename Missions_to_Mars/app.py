from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

#connect to mongo db and collection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mission_db
mars = db.mars
    
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/",code=302)

# Query local Mongo database and pass the mars data into an HTML template to display 
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_info = mars.find_one()

    # Return template and data
    return render_template("index.html",mars_data=mars_info)

if __name__ == "__main__":
    app.run(debug=True)