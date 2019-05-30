#imports for template, posting, and routing
from bottle import Bottle, route, template, post, get, request, run
from gmplot import gmplot
from bs4 import BeautifulSoup
import geocoder
from requests import get
import sqlite3

db = sqlite3.connect("location.db")
c = db.cursor()

#create bottle app instance
app = Bottle()

#big help from github https://github.com/vgm64/gmplot/issues/16
#problem occurs with google no longer allowing key-less api use
#must use beautiful soup file scraping to insert your api key into generated map file
def putkey(htmltxt, apikey, apistring=None):
    """put the apikey in the htmltxt and return soup"""
    if not apistring:
        #string that is apended with key
        apistring = "https://maps.googleapis.com/maps/api/js?key=%s&callback=initialize&libraries=visualization&sensor=true_or_false"
    soup = BeautifulSoup(htmltxt, 'html.parser')
    soup.script.decompose() #remove the existing script tag
    body = soup.body
    src = apistring % (apikey,)
    tscript = soup.new_tag("script", src=src)
    body.insert(-1, tscript)
    return soup

#function runs put key and uses gmplot to create google map using latitude and longitude
def createMap(lat, lon):
        gmap = gmplot.GoogleMapPlotter(lat, lon, 12)

        gmap.draw("mymap.html")

        htmltxt = open("mymap.html", 'r').read()
        soup = putkey(htmltxt, 'AIzaSyB7MczuuYpj1Ldw9Kg55GJbgZjGuXlm0Ao')
        newtxt = soup.prettify()
        open("mymap.html", 'w').write(newtxt)

@app.route('/')
def index():
	return template("pyIndex.html")
	
	result = c.execute("select * from latitudeLongitude")
	
	print(result.fetchall())
@app.route('/getLatitudeLongitude')
def getlatLon():
	return template("getLatLon.html", db = db, c = c)

#post to create map, runs function to create map and then returns mymap html element
@app.post('/getLatitudeLongitude/createMap')
def webMap():
        lat = request.forms.get("latitude")
        lat = float(lat)
        lon = request.forms.get("longitude")
        lon = float(lon)

        createMap(lat, lon)
        
        return template("mymap.html")
@app.post('/getLatitudeLongitude/savePosition')
def savePosition():
		return template("savePosition.html", db = db, c = c)
	

run(app, host='localhost', port=1337, debug = True)


