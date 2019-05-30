from gmplot import gmplot
from bs4 import BeautifulSoup
import geocoder
from requests import get

#use external ipify website to retrieve public ip address in plain text
ip = get('https://api.ipify.org').text

#use geocoder api to query your public ip address for latitude and longitude
g = geocoder.ip(ip)

print(g.latlng)

lat = float(g.latlng[0])
lon = float(g.latlng[1])

print(lat, lon)

#use gmplot to plot google map of your latitude and longitude
gmap = gmplot.GoogleMapPlotter(lat, lon, 12)

gmap.draw("mymap.html")


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

htmltxt = open("mymap.html", 'r').read()
soup = putkey(htmltxt, 'AIzaSyB7MczuuYpj1Ldw9Kg55GJbgZjGuXlm0Ao')
newtxt = soup.prettify()
open("mymap.html", 'w').write(newtxt)
print('\nKey Insertion Completed!!')


