from __future__ import print_function
from flask import Flask, render_template, request, url_for, redirect, flash

import pprint

from backend.distance_calculator import dummy_lists
from backend.distance_calculator import distance_api
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

pp = pprint.PrettyPrinter()

app = Flask(__name__)


app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# do = get_gspread_data()
# do.authenticate()

# PX_PARTNER = os.getenv('PX_PARTNER')
# PX_PASSWORD = os.getenv('PX_PASSWORD')

### --- Utilities --- ###
def geocoder(address):
    geocoder = Nominatim()
    return geocoder.geocode(address)

def ranked_destinations_calculator(destinations, origin, address):
    suitable_destinations = []
    for destination in destinations:
        distance = vincenty((origin.latitude, origin.longitude),
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

        # get the list of destinations from Google Sheets, typically their are more than 500
        # destinations = do.results["clients"]
        destinations = dummy_lists().destinations_from_gsheet

        # Calculate the vincenty distance to each destination, and then return the closest 25, in order of closeness
        ranked_destinations = ranked_destinations_calculator(destinations, origin, address)
        if not ranked_destinations:
            return render_template('home.html',
                               message="The address: <strong>" + address + "</strong> didn\'t return any results, try to reformat it")

        # Send the ranked list to Google Distance Matrix
        calculated_destinations = distance_api(address, ranked_destinations)

        pp.pprint(calculated_destinations)

        # get the 5 best destinations based on their overall rating
        for desination in calculated_destinations:
            overall = desination['drive_distance'] + desination['duration with traffic'] + desination['duration no traffic']
            desination['overall'] = round(overall, 2)

        return render_template('home.html',
                               destinations=calculated_destinations)


if __name__ == '__main__':
    app.run(debug=True)
