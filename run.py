from __future__ import print_function
from flask import Flask, render_template, request
from urllib.request import urlopen
from urllib.parse import urlencode
import pprint
import simplejson
from backend.distance_calculator import dummy_lists
from backend.distance_calculator import distance_api
from backend.sheets_api import get_gspread_data
from geopy.distance import vincenty


pp = pprint.PrettyPrinter()
DEBUG = True
app = Flask(__name__)


app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

if not DEBUG:
    do = get_gspread_data()
    do.authenticate()

# PX_PARTNER = os.getenv('PX_PARTNER')
# PX_PASSWORD = os.getenv('PX_PASSWORD')

## --- Utilities --- ###
# def geocoder(address):
#     geocoder = Nominatim()
#     print(geocoder.geocode(address).latitude)
#     return geocoder.geocode(address)

def geocoder(address):
    origin={}
    API = "AIzaSyARltEJxYPhqjJVAcq1eR-mEveAVCZ0nKY"
    QUERY = address.replace(" ", "%25")
    URL = "https://maps.googleapis.com/maps/api/geocode/json?address="+ QUERY +"&key="+ API
    response = simplejson.load(urlopen(URL))
    print(URL)

    if response['status'] != "OK":
        origin['status'] = response['status']
        return origin
    origin['status'] = response['status']
    origin['longitude'] = response['results'][0]['geometry']['location']['lng']
    origin['latitude'] = response['results'][0]['geometry']['location']['lat']
    origin['formatted_address'] = response['results'][0]['formatted_address']
    origin['given_address'] = address

    return origin

def ranked_destinations_calculator(destinations, origin):
    suitable_destinations = []
    for destination in destinations:
        distance = vincenty((origin['latitude'], origin['longitude']),
                                           (destination['Lat'], destination['Lon'])).kilometers
        # filter out distances which are too far
        if distance >= 50:
            print('distance to great')
            continue
        else:
            destination["Distance"] = distance
            suitable_destinations.append(destination)

    ranked_destination = sorted(suitable_destinations, key=lambda user: user['Distance'])[:25]

    return ranked_destination

@app.route('/', methods=['GET', 'POST'])
def filter_client_db():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # get the origin address from the form
        address = request.form['address']
        print('got address:', address)

        # geocode the address into latitude and longitude coordinates
        origin = geocoder(address)
        if origin['status'] != "OK":
            print("status not OK")
            return render_template('home.html', message=origin['status'])

        # get the list of destinations from Google Sheets, typically their are more than 500
        destinations = do.results["clients"] if not DEBUG else dummy_lists().destinations_from_gsheet


        # Calculate the vincenty distance to each destination, and then return the closest 25, in order of closeness
        ranked_destinations = ranked_destinations_calculator(destinations, origin)

        if not ranked_destinations:
            return render_template('home.html',
                               message="The address: <strong>" + address + "</strong> didn\'t return any results, try to reformat it")

        # Send the ranked list to Google Distance Matrix
        calculated_destinations = distance_api(address, ranked_destinations) if not DEBUG else dummy_lists().destinations

        # if calculated_destinations['error']:
        #     return render_template('home.html', message=calculated_destinations['error'])

        # get the 5 best destinations based on their overall rating
        for desination in calculated_destinations:
            overall = desination['drive_distance'] + desination['duration with traffic'] + desination['duration no traffic']
            desination['overall'] = round(overall, 2)

        return render_template('home.html',
                               destinations=calculated_destinations, origin=origin)

if __name__ == '__main__':
    app.run(debug=True)
