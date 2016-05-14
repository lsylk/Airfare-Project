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
    #The forllowing variables are defined to call different keys from the dictionary returned from the post request:
    # number of results is a list

        trip_options = search_flights_json["trips"]["tripOption"]  # trip_options is a list of dictionaries, one dictionary per option.

        departure_date = trip_options[i]["slice"][0]["segment"][0]["leg"][0]["departureTime"]  # returns a str
        # date = datetime.strptime(departure_date, '%Y-%m-%dT%H:%M+%S:%f')
        # departure_date = date.strftime("%A, %d %B %Y")
        # departure_time = date.strftime("%I:%M%p")

        arrival_date = trip_options[i]["slice"][0]["segment"][0]["leg"][0]["arrivalTime"]  # returns a str
        # date = datetime.strptime(arrival_date, '%Y-%m-%dT%H:%M+%S:%f')
        # arrival_date = date.strftime("%A, %d %B %Y")
        # arrival_time = date.strftime("%I:%M%p")

        flight_duration = str(trip_options[i]["slice"][0]["duration"])  # returns an int -> type casted to a str
        sale_fare_total = trip_options[i]["pricing"][0]["saleFareTotal"]  # returns a str
        sale_tax_total = trip_options[i]["pricing"][0]["saleTaxTotal"]  # returns a str
        sale_total = trip_options[i]["pricing"][0]["saleTotal"]  # returns a str

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        data = search_flights_json["trips"]["data"]  # data is a nested object

        aircraft_name = data["aircraft"][0]["name"]  # returns a str
        carrier_code = data["carrier"][0]["code"]  # returns a str
        carrier_name = data["carrier"][0]["name"]  # returns a str
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


        # #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # data = search_flights_json["trips"]["data"]  # data is a nested object


        # aircraft_name = data["aircraft"][i]["name"]  # returns a str
        # carrier_code = data["carrier"][i]["code"]  # returns a str
        # carrier_name = data["carrier"][i]["name"]  # returns a str

        results = [departure_date,
                   # departure_time,
                   airport_code_departure,
                   airport_name_departure,
                   arrival_date,
                   # arrival_time,
                   airport_code_arrival,
                   airport_name_arrival,
                   carrier_name,
                   carrier_code,
                   aircraft_name,
                   flight_duration,
                   sale_fare_total,
                   sale_tax_total,
                   sale_total]

        all_results.append(results)

        datetime = [departure_date, arrival_date]

        datetime_object = instantiate_datetime_object(datetime)


# r = json.dumps(search_results)
# print r

# example = [{ "name": "Nick" }, {"name": "Leslye"}]

################


# num_free_baggagge = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["pieces"]
# free_baggage_weigh = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["kilosPerPieces"]

    return all_results  # it's a list of lists


def instantiate_datetime_object(datetime):
    """Takes a date as a string and instatiates it into an object."""


    parse_date_format = "%Y-%m-%dT%H:%M-%S:%f"

    all_datetime = []
    for i in datetime:

        datetime_object = datetime.strptime(date[i], parse_date_format)

        all_datetime.append(datetime_object)

    return all_datetime


def format_datetime_object(all_datetime):
    """Takes a datetime object and returns a string to represent the date and time."""

    for datetime_object in all_datetime:
        date_stamp = datetime_object.strftime("%A, %d %B %Y")
        time_stamp = datetime_object.strftime("%I:%M%p")

    return date_stamp, time_stamp  # returns a tupple




#     all_results = []
#     for i in range(int(number_of_results)):
#     #The forllowing variables are defined to call different keys from the dictionary returned from the post request:

#         trip_options = search_results["trips"]["tripOption"]  # trip_options is a list of dictionaries, one dictionary per option.

#         departure_date = trip_options[i]["slice"][0]["segment"][0]["leg"][0]["departureTime"]  # returns a str
#         datetime_object = datetime.strptime(departure_date, '%Y-%m-%dT%H:%M-%S:%f')
#         departure_date = date.strftime("%A, %d %B %Y")
#         departure_time = date.strftime("%I:%M%p")

#         arrival_date = trip_options[i]["slice"][0]["segment"][0]["leg"][0]["arrivalTime"]  # returns a str
#         date = datetime.strptime(arrival_date, '%Y-%m-%dT%H:%M-%S:%f')
#         arrival_date = date.strftime("%A, %d %B %Y")
#         arrival_time = date.strftime("%I:%M%p")

#         flight_duration = str(trip_options[i]["slice"][0]["duration"])  # returns an int -> type casted to a str
#         sale_fare_total = trip_options[i]["pricing"][0]["saleFareTotal"]  # returns a str
#         sale_tax_total = trip_options[i]["pricing"][0]["saleTaxTotal"]  # returns a str
#         sale_total = trip_options[i]["pricing"][0]["saleTotal"]  # returns a str


#         #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#         data = search_results["trips"]["data"]  # data is a nested object

#         aircraft_name = data["aircraft"][i]["name"]  # returns a str
#         carrier_code = data["carrier"][i]["code"]  # returns a str
#         carrier_name = data["carrier"][i]["name"]  # returns a str

#         results = [departure_date,
#                    departure_time,
#                    airport_code_departure,
#                    airport_name_departure,
#                    arrival_date,
#                    arrival_time,
#                    airport_code_arrival,
#                    airport_name_arrival,
#                    carrier_name,
#                    carrier_code,
#                    aircraft_name,
#                    flight_duration,
#                    sale_fare_total,
#                    sale_tax_total,
#                    sale_total]

#         # booger

#         all_results.append(results)


#     # r = json.dumps(search_results)
#     # print r

#     # example = [{ "name": "Nick" }, {"name": "Leslye"}]

#     return render_template("airfares.html",
#                            all_results=all_results)


# ################




# # num_free_baggagge = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["pieces"]
# # free_baggage_weigh = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["kilosPerPieces"]

# if __name__ == "__main__":
#     # We have to set debug=True here, since it has to be True at the point
#     # that we invoke the DebugToolbarExtension
#     app.debug = True

#     # connect_to_db(app)

#     # Use the DebugToolbar
#     DebugToolbarExtension(app)

#     app.run()
