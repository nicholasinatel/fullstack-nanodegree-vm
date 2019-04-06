import httplib2
import json


def getGeocodeLocation(inputString):
    google_api_key = "AIzaSyAwb-__2M4kuvmelq3CI7FIfZjV0ZglKi4"
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
    h = httplib2.Http() # Create Instace of Http Class
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    print "response header: %s \n \n" % response
    return result

def parseLocation(response):
    latitude = response['results'][0]['geometry']['location']['lat']
    longitude = response['results'][0]['geometry']['location']['lng']
    print "latitude: %s" % latitude
    print "longitude: %s" % longitude



parseLocation(getGeocodeLocation("Dallas, Texas"))