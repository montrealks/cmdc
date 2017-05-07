from flask import Flask, render_template, request
from project.utilities.utilities import *
import simplejson
from project.google_apis.distance_calculator import distance_api
from project.google_apis.sheets_api import get_gspread_data
from project.settings.settings import *

app = Flask(__name__)

@app.route('/map', methods=['GET', 'POST'])
def display_map():
    destinations = {}
    destinations[1] = {'lat': 45.364, 'lng': -73.5700}
    destinations[2] = {'lat': 45.363, 'lng': -73.5644}
    d = simplejson.dumps(destinations)


    return render_template('map.html', d=d)

@app.route('/', methods=['GET', 'POST'])
def filter_client_db():
    if request.method == 'GET':
        return render_template('results.html')
    else:
        print("POST")
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
            return render_template('results.html', message=origin['status'])
        else:
            print("Geocode successful.")


        ############################################################
        # Get destinations from API or local dummy
        ############################################################
        gspread_api = get_gspread_data()
        print("Getting the list of destinations from", gspread_api.source)
        destinations= gspread_api.destinations['clients']
        print("Got", gspread_api.source, "destinations. Length: ", len(destinations))


        ############################################################
        # Calculate the vincenty distance to each destination
        # Return the closest 25, in order of closeness
        ############################################################
        print("sending destinations to get ranked in order of closeness to", origin['formatted_address'])
        ranked_destinations = ranked_destinations_calculator(destinations, origin)
        if not ranked_destinations:
            return render_template('results.html',
                               message="The address: <strong>" + address + "</strong> didn\'t return any results, try to reformat it")
        print("The destinations are ranked and trimmed")




        ############################################################
        # Get distances and durations from API or local dummy
        ############################################################
        print("Sending the ranked list to the distance matrix")
        calculated_destinations = distance_api(address, ranked_destinations)
        if "error" in calculated_destinations:
            return render_template('results.html', message=calculated_destinations['error'])
        print("calculated destinations", len(calculated_destinations))


        ############################################################
        # Rank each calculated distance
        ############################################################
        destinations_with_overall = destination_overall_rank(calculated_destinations)
        geo_origin = simplejson.dumps(origin)



        geod = {}
        geod['destinations'] = []
        for item in destinations_with_overall:
            # geocoded = geocoder(item['formatted address'])
            # item['Lat'], item["Lon"] = geocoded['latitude'], geocoded['longitude']

            geod['destinations'].append(item)

        geod_sanitized = simplejson.dumps(geod).replace("'", "\\\'")

        return render_template('results.html',
                               destinations=destinations_with_overall,
                               origin=origin,
                               geod=geod_sanitized,
                               geo_origin=geo_origin)



app.run(debug=True) if __name__ == '__main__' and LOCAL_RUN else None


