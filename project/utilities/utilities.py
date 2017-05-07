__author__ = "Kris"
from unicodedata import normalize
from urllib.request import urlopen
import simplejson
from geopy.distance import vincenty
from project.settings.settings import CMDC_API
from project.google_apis.sheets_api import GOOGLE_SHEETS_DUMMY_LIST
from project.settings.settings import pp


def geocoder(address):
    origin = {}
    query = accent_cleaner(address.replace(" ", "%25"))
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + query + "&key=" + CMDC_API
    print("%%%% Geocoder %%%% Attempting geocode API at:", url)
    response = simplejson.load(urlopen(url))


    if response['status'] != "OK":
        origin['status'] = response['status']
        return origin
    origin['status'] = response['status']
    origin['longitude'] = response['results'][0]['geometry']['location']['lng']
    origin['latitude'] = response['results'][0]['geometry']['location']['lat']
    origin['formatted_address'] = response['results'][0]['formatted_address']
    origin['given_address'] = address

    print("%%%% Geocoder %%%% given address: ", address, "resolves as:", origin['formatted_address'])

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

def destination_overall_rank(calculated_destinations):
    for destination in calculated_destinations:
            if isinstance(destination['duration with traffic'], float):
                overall = destination['drive_distance'] + destination['duration no traffic'] + destination['duration with traffic']
            else:
                overall = destination['drive_distance'] + destination['duration no traffic']
            destination['overall'] = round(overall, 2)
    return calculated_destinations


def accent_cleaner(accented_string):
    """
    Remove all french accents from the address values

    :param accented_string: string containing characters which need to be normalized
    :return: Normalized string, ok for url encoding
    """
    return normalize('NFKD', accented_string).encode('ASCII', 'ignore').decode()

def add_montreal(destinations):
    """
    Find address values that are not yet localized to Montreal.
    This helps Google return accurate locations
    :param destinations: the dictionary containing the address values
    :return:
    """
    d = ""
    for address in destinations:
        if ("Montreal" or "montreal" or "Montréal" or "montréal") not in address['Address']:
            address['Address'] += ", Montreal"
        d += address['Address'].replace(" ", "+") + "|"

    return d



def dummy_list_geocoder(dummy_list):
    new_dummy_list = {}
    new_dummy_list["clients"] = []
    failed_list = {}
    failed_list['clients'] = []
    counter = 1
    for destination in dummy_list['clients']:
        # Add montreal if not already present
        counter += 1
        print(counter)
        if ("Montreal" or "montreal" or "Montréal" or "montréal") not in destination['Address']:
            destination['Address'] += ", Montreal"

        # escape single quotes
        destination['Address'].replace("'", "\\\'")

        # clean up the url
        destination['Address'].replace(" ", "+")

        # Send to geocoder
        geo_coords = geocoder(destination['Address'])

        if geo_coords['status'] != "OK":
            failed_list['clients'].append(geo_coords)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            continue

        # load results into the new dummy list
        destination['Lat'], destination['Lon'], destination['formatted address'] = geo_coords['latitude'], geo_coords['longitude'], geo_coords['formatted_address']

        new_dummy_list["clients"].append(destination)

    pp.pprint(new_dummy_list)

