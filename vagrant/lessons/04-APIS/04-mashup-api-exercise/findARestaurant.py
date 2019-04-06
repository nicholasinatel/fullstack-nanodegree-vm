from geocode import getGeocodeLocation
import json
import httplib2, requests

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "EE24NJZ4PU4LJAG2NUDL3GHV55CQJ0VHM20VIM5G1UXYLRKT"
foursquare_client_secret = "I4E51LOHGMUY5XKL24YVXUWDQQT55QGLHHVFJOBAFJ5OXOE1"


def findARestaurant(mealType,location):
    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    result = getGeocodeLocation(location)
    latitude = result[0]
    longitude = result[1]
    print "latitude: %d, longitude: %d" % (latitude, longitude)

    #2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    #HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = 'https://api.foursquare.com/v2/venues/explore'

    params = dict(
    client_id=foursquare_client_id,
    client_secret=foursquare_client_secret,
    v='20180323',
    # ll='40.7243,-74.0018',
    ll='{},{}'.format(latitude,longitude),
    query=mealType,
    limit=1
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    #3. Grab the first restaurant
    first_restaurant = data['response']['groups'][0]['items'][0]['venue']['name']
    print "first_restaurant: %s" % first_restaurant 
    #4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    
    #5. Grab the first image
    #6. If no image is available, insert default a image url
    #7. Return a dictionary containing the restaurant name, address, and image url	

    return 200







if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney, Australia")