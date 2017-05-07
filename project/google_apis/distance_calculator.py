from unicodedata import normalize
from urllib.parse import urlencode
from urllib.request import urlopen
import simplejson
from project.settings.settings import *
from project.utilities.utilities import add_montreal
from project.utilities.utilities import accent_cleaner


def distance_api(origin, destinations, **geo_args):

    ############################################################
    # Build the URL for all destinations using their ADDRESS
    ############################################################



    d = add_montreal(destinations)

    ############################################################
    # Clean the accents
    ############################################################
    a = accent_cleaner(d)


    ############################################################
    # Get a response from the Google Distance Matrix API
    ############################################################

    geo_args.update({
        'origins': origin,
        'traffic_model': TRAFFIC_MODEL,
        'departure_time': int(DEPARTURE_TIME.timestamp()),
        'mode': MODE,
        'destinations': a,
        'key': CMDC_API
    })

    # unpack geoargs to create the API url
    url = GEOCODE_BASE_URL + '?' + urlencode(geo_args)
    print("%%%% distance_api %%%%", "Distance matrix API URL:", url)
    # load results from the API or from the DUMMY list
    results = simplejson.load(urlopen(url)) if DISTANCE_MATRIX == "api" else DISTANCE_MATRIX_RESPONSE_DUMMY_LIST

    # Validate the reuslts
    if results["status"] != "OK":
        return error_checker(results)


    ############################################################
    # Add the duration and distance results to 'destinations'
    ############################################################
    updated_destinations = destinations_updater(results, destinations)
    if len(updated_destinations) is 0:
        print("ERROR: Google could not find a path in between the address and any clients. Try a new address")
        return False

    return updated_destinations



def error_checker(results):
    destinations = {}
    destinations['status'] = results["status"]
    destinations['error'] = results["error_message"] if "error" in results else None
    print("Google Distance API status: ", results['status'], "\n Google Distance API error message:", results['error'])
    return destinations

def destinations_updater(results, destinations):
    i = -1
    # get the number of results
    results_length = len(results['rows'][0]['elements'])

    print("results length:", results_length)
    for result in results['rows'][0]['elements']:
        i += 1
        if results['rows'][0]['elements'][0]['status'] != 'OK':
            print('couldn\'nt find a route')
            del destinations[i]
            continue
        formatted_address = results['destination_addresses'][i]
        distance = round(result['distance']['value'] / 1000, 3)  # km
        duration = round(result['duration']['value'] / 60, 3)  # minutes
        duration_in_traffic = round(result['duration_in_traffic']['value'] / 60, 3) if 'duration_in_traffic' in result else "No traffic Data available"  # minutes
        durations = {"drive_distance": distance,
                     "duration no traffic": duration,
                     "duration with traffic": duration_in_traffic,
                     "formatted address": formatted_address}
        destinations[i].update(durations)


    return destinations[:results_length]


DISTANCE_MATRIX_RESPONSE_DUMMY_LIST = {
            "destination_addresses": [
                "241 Rue Maria, Montréal, QC H4C 2N6, Canada",
                "241 Rue Maria, Montréal, QC H4C 2N6, Canada",
                "241 Rue Maria, Montréal, QC H4C 2N6, Canada",
                "313 Rue Maria, Montréal, QC H4C, Canada",
                "3970-4000 Rue Saint-Ambroise, Montréal, QC H4C 2E1, Canada",
                "3985 Rue Notre-Dame Ouest, Montréal, QC H4C 1R2, Canada",
                "256 Rue Saint-Ferdinand, Montreal, QC H4C 2S8, Canada",
                "3632 Notre-Dame ouest, Montréal, Quebec, Canada, Montreal",
                "3632 Notre-Dame ouest, Montréal, Quebec, Canada, Montreal",
                "211-295 Rose of Lima St, Montreal, QC H4C, Canada",
                "211-295 Rose of Lima St, Montreal, QC H4C, Canada",
                "4291 Rue Saint-Ambroise, Montréal, QC H4C 2E4, Canada",
                "715-815 Rue Bel Air, Montréal, QC H4C, Canada",
                "3713-3899 Rue Saint-Antoine O, Montréal, QC H4C 2P4, Canada",
                "3713-3899 Rue Saint-Antoine O, Montréal, QC H4C 2P4, Canada",
                "780-800 Brewster Ave, Montreal, QC H4C 2K1, Canada",
                "Boulevard Ville-Marie, Westmount, QC H3Z, Canada",
                "2461-2645 Fauteux St, Montreal, QC H3J, Canada",
                "2461-2645 Fauteux St, Montreal, QC H3J, Canada",
                "2207-2229 Avenue Hawarden, Montréal, QC H3H, Canada",
                "2365 Rue Grand Trunk, Montréal, QC H3K 1M8, Canada",
                "Boulevard René-Lévesque O & Autoroute Ville-Marie & Autoroute 720, Montréal, QC H3H, Canada",
                "2035-2045 Rue Lambert Closse, Montréal, QC H3H 1Z7, Canada",
                "460 Avenue Wood, Westmount, QC H3Y 3J2, Canada",
                "460 Avenue Wood, Westmount, QC H3Y 3J2, Canada"
            ],
            "origin_addresses": ["209A Rue Maria, Montréal, QC H4C, Canada"],
            "rows": [
                {
                    "elements": [
                        {
                            "distance": {
                                "text": "76 m",
                                "value": 76
                            },
                            "duration": {
                                "text": "1 min",
                                "value": 23
                            },
                            "duration_in_traffic": {
                                "text": "1 min",
                                "value": 22
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "76 m",
                                "value": 76
                            },
                            "duration": {
                                "text": "1 min",
                                "value": 23
                            },
                            "duration_in_traffic": {
                                "text": "1 min",
                                "value": 22
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "76 m",
                                "value": 76
                            },
                            "duration": {
                                "text": "1 min",
                                "value": 23
                            },
                            "duration_in_traffic": {
                                "text": "1 min",
                                "value": 22
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.2 km",
                                "value": 184
                            },
                            "duration": {
                                "text": "1 min",
                                "value": 55
                            },
                            "duration_in_traffic": {
                                "text": "1 min",
                                "value": 55
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.8 km",
                                "value": 787
                            },
                            "duration": {
                                "text": "3 mins",
                                "value": 207
                            },
                            "duration_in_traffic": {
                                "text": "4 mins",
                                "value": 214
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.4 km",
                                "value": 378
                            },
                            "duration": {
                                "text": "2 mins",
                                "value": 125
                            },
                            "duration_in_traffic": {
                                "text": "2 mins",
                                "value": 137
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.3 km",
                                "value": 1267
                            },
                            "duration": {
                                "text": "5 mins",
                                "value": 296
                            },
                            "duration_in_traffic": {
                                "text": "5 mins",
                                "value": 312
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.4 km",
                                "value": 401
                            },
                            "duration": {
                                "text": "2 mins",
                                "value": 126
                            },
                            "duration_in_traffic": {
                                "text": "2 mins",
                                "value": 142
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.4 km",
                                "value": 401
                            },
                            "duration": {
                                "text": "2 mins",
                                "value": 126
                            },
                            "duration_in_traffic": {
                                "text": "2 mins",
                                "value": 142
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.5 km",
                                "value": 483
                            },
                            "duration": {
                                "text": "3 mins",
                                "value": 178
                            },
                            "duration_in_traffic": {
                                "text": "3 mins",
                                "value": 199
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.5 km",
                                "value": 483
                            },
                            "duration": {
                                "text": "3 mins",
                                "value": 178
                            },
                            "duration_in_traffic": {
                                "text": "3 mins",
                                "value": 199
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.1 km",
                                "value": 1141
                            },
                            "duration": {
                                "text": "4 mins",
                                "value": 263
                            },
                            "duration_in_traffic": {
                                "text": "5 mins",
                                "value": 281
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "0.9 km",
                                "value": 851
                            },
                            "duration": {
                                "text": "5 mins",
                                "value": 285
                            },
                            "duration_in_traffic": {
                                "text": "5 mins",
                                "value": 323
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.2 km",
                                "value": 1183
                            },
                            "duration": {
                                "text": "6 mins",
                                "value": 331
                            },
                            "duration_in_traffic": {
                                "text": "6 mins",
                                "value": 378
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.2 km",
                                "value": 1183
                            },
                            "duration": {
                                "text": "6 mins",
                                "value": 331
                            },
                            "duration_in_traffic": {
                                "text": "6 mins",
                                "value": 378
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.3 km",
                                "value": 1324
                            },
                            "duration": {
                                "text": "7 mins",
                                "value": 430
                            },
                            "duration_in_traffic": {
                                "text": "8 mins",
                                "value": 482
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "9.8 km",
                                "value": 9844
                            },
                            "duration": {
                                "text": "17 mins",
                                "value": 1043
                            },
                            "duration_in_traffic": {
                                "text": "24 mins",
                                "value": 1433
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.2 km",
                                "value": 1191
                            },
                            "duration": {
                                "text": "6 mins",
                                "value": 380
                            },
                            "duration_in_traffic": {
                                "text": "8 mins",
                                "value": 465
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.2 km",
                                "value": 1191
                            },
                            "duration": {
                                "text": "6 mins",
                                "value": 380
                            },
                            "duration_in_traffic": {
                                "text": "8 mins",
                                "value": 465
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "1.6 km",
                                "value": 1580
                            },
                            "duration": {
                                "text": "7 mins",
                                "value": 390
                            },
                            "duration_in_traffic": {
                                "text": "9 mins",
                                "value": 522
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "2.4 km",
                                "value": 2357
                            },
                            "duration": {
                                "text": "10 mins",
                                "value": 572
                            },
                            "duration_in_traffic": {
                                "text": "12 mins",
                                "value": 701
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "10.7 km",
                                "value": 10653
                            },
                            "duration": {
                                "text": "18 mins",
                                "value": 1100
                            },
                            "duration_in_traffic": {
                                "text": "25 mins",
                                "value": 1499
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "2.2 km",
                                "value": 2189
                            },
                            "duration": {
                                "text": "9 mins",
                                "value": 526
                            },
                            "duration_in_traffic": {
                                "text": "12 mins",
                                "value": 726
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "2.6 km",
                                "value": 2603
                            },
                            "duration": {
                                "text": "10 mins",
                                "value": 587
                            },
                            "duration_in_traffic": {
                                "text": "14 mins",
                                "value": 830
                            },
                            "status": "OK"
                        },
                        {
                            "distance": {
                                "text": "2.6 km",
                                "value": 2603
                            },
                            "duration": {
                                "text": "10 mins",
                                "value": 587
                            },
                            "duration_in_traffic": {
                                "text": "14 mins",
                                "value": 830
                            },
                            "status": "OK"
                        }
                    ]
                }
            ],
            "status": "OK"
        }

