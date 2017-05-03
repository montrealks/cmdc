from __future__ import print_function
from flask import Flask, render_template, request, session
from urllib.request import urlopen
import pprint
import simplejson
from backend.distance_calculator import dummy_lists
from backend.distance_calculator import distance_api
from backend.sheets_api import get_gspread_data
from geopy.distance import vincenty
pp = pprint.PrettyPrinter()

app = Flask(__name__)

# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

def initialize_sheets_api():
    do = get_gspread_data()
    do.authenticate()

    return do.results['clients']

############################################################
# SETTINGS
############################################################
destinations_from_google_spread_sheet = 'dummy'




############################################################
# Don't Touch
############################################################
DESTINATIONS = dummy_lists().destinations_from_gsheet if destinations_from_google_spread_sheet == "dummy" else initialize_sheets_api()


def geocoder(address):
    origin={}
    API = "AIzaSyARltEJxYPhqjJVAcq1eR-mEveAVCZ0nKY"
    QUERY = address.replace(" ", "%25")
    URL = "https://maps.googleapis.com/maps/api/geocode/json?address="+ QUERY +"&key="+ API
    print("Attempting geocode API at:", URL)
    response = simplejson.load(urlopen(URL))

    if response['status'] != "OK":
        origin['status'] = response['status']
        return origin
    origin['status'] = response['status']
    origin['longitude'] = response['results'][0]['geometry']['location']['lng']
    origin['latitude'] = response['results'][0]['geometry']['location']['lat']
    origin['formatted_address'] = response['results'][0]['formatted_address']
    origin['given_address'] = address
    print("given address: ", address, "resolves as:", origin['formatted_address'])

    return origin


def ranked_destinations_calculator(destinations, origin):
    suitable_destinations = []
    for destination in destinations:
        distance = vincenty((origin['latitude'], origin['longitude']), (destination['Lat'], destination['Lon'])).kilometers
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
        ############################################################
        # Get address from the form
        ############################################################
        address = request.form['address']
        print('got address:', address)



        ############################################################
        # Geocode the provided address
        ############################################################
        print("Beginning to geocode the origin", address)
        origin = geocoder(address)
        if origin['status'] != "OK":
            print("Geocode API failed with status:", origin['status'])
            return render_template('home.html', message=origin['status'])
        else:
            print("Geocode successful.")



        ############################################################
        # Get destinations from API or local dummy
        ############################################################
        print("Getting the list of destinations from", "dummy" if DESTINATIONS == "dummy" else "API")
        destinations = DESTINATIONS
        print("Got destinations list from", "dummy" if DESTINATIONS == "dummy" else "API", "\nDestinations length:", len(destinations))


        ############################################################
        # Calculate the vincenty distance to each destination
        # Return the closest 25, in order of closeness
        ############################################################
        print("sending destinations to get ranked in order of closeness to", origin['formatted_address'])
        ranked_destinations = ranked_destinations_calculator(destinations, origin)
        if not ranked_destinations:
            return render_template('home.html',
                               message="The address: <strong>" + address + "</strong> didn\'t return any results, try to reformat it")
        print("The destinations are ranked and trimmed")




        ############################################################
        # Get distances and durations from API or local dummy
        ############################################################
        print("Sending the ranked list to the distance matrix")
        calculated_destinations = distance_api(address, ranked_destinations)
        if "error" in calculated_destinations:
            return render_template('home.html', message=calculated_destinations['error'])
        print("calculated destinations", len(calculated_destinations))



        ############################################################
        # Rank each calculated distance
        ############################################################
        for destination in calculated_destinations:
            if isinstance(destination['duration with traffic'], float):
                overall = destination['drive_distance'] + destination['duration no traffic'] + destination['duration with traffic']
            else:
                overall = destination['drive_distance'] + destination['duration no traffic']
            destination['overall'] = round(overall, 2)

        return render_template('home.html',
                               destinations=calculated_destinations, origin=origin)

if __name__ == '__main__':
    app.run(debug=True)
