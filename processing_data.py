from os import environ

import requests

from flask import request

import json

from datetime import datetime


def request_user_input():
    """Requests user's input information at /."""

    departure = request.form.get("departure")
    arrival = request.form.get("arrival")
    departure_date = request.form.get("departure-date")
    arrival_date = request.form.get("arrival-date")
    number_of_results = request.form.get("results")

    input_result = [departure, arrival, departure_date, arrival_date, number_of_results]

    return input_result


def search_flights(request_inputs):
    """Makes an API call and searches for flights based on user's input information."""

    API_KEY = environ['AIRFARE_USER_KEY']

    # HTTP request to google's API QPX
    REQUEST_URL = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + API_KEY

    # Structure of the request body
    payload = {
        "request": {
            "passengers": {
                "kind": "qpxexpress#passengerCounts",
                "adultCount": 1,
                "childCount": 0,
                "infantInLapCount": 0,
                "infantInSeatCount": 0,
                "seniorCount": 0
            },
            "slice": [
                {
                    "kind": "qpxexpress#sliceInput",
                    "origin": str(request_inputs[0]),
                    "destination": str(request_inputs[1]),
                    "date": str(request_inputs[2]),
                    "maxStops": 0,
                    "maxConnectionDuration": 0,
                    "preferredCabin": None,
                    "permittedDepartureTime": {
                        "kind": "qpxexpress#timeOfDayRange",
                        "earliestTime": None,
                        "latestTime": None
                        },
                    "permittedCarrier": [
                        None
                    ],
                    "alliance": None,
                    "prohibitedCarrier": [
                        None
                    ]
                    }
                ],
            "maxPrice": None,
            "saleCountry": None,
            "refundable": False,
            "solutions": int(request_inputs[4]),
            }
        }

    # Dump is data taken from a storage medium.
    # UTF-8 is a character encoding capable of encoding all possible characters, or code points, defined by Unicode. The encoding is variable-length and uses 8-bit code units.

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    headers = {"Content-Type": "application/json"}

    r = requests.post(REQUEST_URL, data=json.dumps(payload), headers=headers)  # Used post method request and json.dumps to turn the dictionary into a JSON string

    search_results = r.json()

    ra = json.dumps(search_results)
    print ra

    return search_results


def processing_data(search_flights_json, request_inputs):
    """Processes the results from the user's search"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cities = search_flights_json["trips"]["data"]["city"]  # cities is a list

    airport_code_departure = cities[0]["code"]  # returns a str
    airport_name_departure = cities[0]["name"]  # returns a str
    airport_code_arrival = cities[1]["code"]  # returns a str
    airport_name_arrival = cities[1]["name"]  # returns a str

    all_results = []
    for i in range(int(request_inputs[4])):
    # The following variables are defined to call different keys from the dictionary returned from the post request:
    # number of results is a list

        trip_options = search_flights_json["trips"]["tripOption"]  # trip_options is a list of dictionaries, one dictionary per option.

        departure_date = trip_options[i]["slice"][0]["segment"][0]["leg"][0]["departureTime"]  # returns a str
        arrival_date = trip_options[i]["slice"][0]["segment"][0]["leg"][0]["arrivalTime"]  # returns a str

        sale_fare_total = trip_options[i]["pricing"][0]["saleFareTotal"]  # returns a str
        sale_tax_total = trip_options[i]["pricing"][0]["saleTaxTotal"]  # returns a str
        sale_total = trip_options[i]["pricing"][0]["saleTotal"]  # returns a str

        flight_duration = str(trip_options[i]["slice"][0]["duration"])  # returns an int -> type casted to a str
        aircraft_number = trip_options[i]["slice"][0]["segment"][0]["flight"]["number"]  # returns a str
        carrier_code = trip_options[i]["slice"][0]["segment"][0]["flight"]["carrier"]  # returns a str

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        data = search_flights_json["trips"]["data"]  # data is a nested object

        carrier_name_code = data["carrier"][0]["code"]  # returns a str
        carrier_name = data["carrier"][0]["name"]

        if carrier_code == carrier_name_code:
            carrier_name = data["carrier"][0]["name"]
        else:
            carrier_name = data["carrier"][1]["name"]

        datetime_stamps = [departure_date, arrival_date]  # [u'2016-09-10T15:35-07:00', u'2016-09-10T16:48-07:00']

        datetime_objects = instantiate_datetime_object(datetime_stamps)  # [datetime.datetime(2016, 9, 10, 15, 35, 7), datetime.datetime(2016, 9, 10, 16, 48, 7)]

        datetime_stamps = format_datetime_object(datetime_objects)  # [('Saturday, 10 September 2016', '03:35PM'), ('Saturday, 10 September 2016', '04:48PM')]

        # all_results_with_datestamps = (all_results, datetime_stamps)
# #########################################################################
############################################################################
        # trip_options = search_flights_json["trips"]["tripOption"][i]  # trip_options is a list of dictionaries, one dictionary per option.
        # slice_0 = ["slice"][0]["segment"][0]["leg"][0]
        # pricing_0 = ["pricing"][0]

        # departure_date = trip_options[i][slice_0]["departureTime"]  # returns a str
        # datetime_object = datetime.strptime(departure_date, parse_date_format)

        # arrival_date = trip_options[i][slice_0]["arrivalTime"]  # returns a str

        # flight_duration = str(trip_options["slice_0"]["duration"])  # returns an int -> type casted to a str
        # sale_fare_total = trip_options["pricing_0"]["saleFareTotal"]  # returns a str
        # sale_tax_total = trip_options["pricing_0"]["saleTaxTotal"]  # returns a str
        # sale_total = trip_options["pricing_0"]["saleTotal"]  # returns a str

        departure_date = datetime_stamps[0][0]
        departure_time = datetime_stamps[0][1]
        arrival_date = datetime_stamps[1][0]
        arrival_time = datetime_stamps[1][1]

        results = [departure_date,
                   departure_time,
                   airport_code_departure,
                   airport_name_departure,
                   arrival_date,
                   arrival_time,
                   airport_code_arrival,
                   airport_name_arrival,
                   carrier_name,
                   carrier_code,
                   aircraft_number,
                   flight_duration,
                   sale_fare_total,
                   sale_tax_total,
                   sale_total]

        all_results.append(results)

        # booger
      

# r = json.dumps(search_results)
# print r

################


# num_free_baggagge = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["pieces"]
# free_baggage_weigh = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["kilosPerPieces"]
     

    return all_results


def instantiate_datetime_object(datetime_stamps):
    """Takes a date as a string and instatiates it into an object."""

    parse_date_format = "%Y-%m-%dT%H:%M-%S:%f"

    all_datetime_stamps = []

    for datetime_stamp in datetime_stamps:
        datetime_object = datetime.strptime(datetime_stamp, parse_date_format)
        all_datetime_stamps.append(datetime_object)

    return all_datetime_stamps


def format_datetime_object(datetime_stamps):
    """Takes a datetime object and returns a string to represent the date and time."""

    all_date_time_stamps = []

    for datetime_object in datetime_stamps:
        date_stamp = datetime_object.strftime("%A, %d %B %Y")
        time_stamp = datetime_object.strftime("%I:%M%p")
        all_date_time_stamps.append((date_stamp, time_stamp))

    return all_date_time_stamps  # returns a tupple
