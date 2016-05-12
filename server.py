import os

import requests

import json

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime

# from model import

from pprint import pprint

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Raises an error if an undefined variable in Jinja2 fails silently.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def search():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/results', methods=["POST"])
def airfares():
    """Results from search."""

    departure = request.form.get("departure")
    arrival = request.form.get("arrival")
    departure_date = request.form.get("departure-date")
    arrival_date = request.form.get("arrival-date")
    number_of_results = request.form.get("results")

    API_KEY = os.environ['AIRFARE_USER_KEY']

    # HTTP request
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
                    "origin": departure,
                    "destination": arrival,
                    "date": departure_date,
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
            "solutions": number_of_results,
            }
        }

    # Dump is data taken from a storage medium.
    # UTF-8 is a character encoding capable of encoding all possible characters, or code points, defined by Unicode. The encoding is variable-length and uses 8-bit code units.

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    headers = {"Content-Type": "application/json"}

    # Asking for a request using the post method
    # Used json.dumps to turn the dictionary into a JSON string
    r = requests.post(REQUEST_URL, data=json.dumps(payload), headers=headers)
    search_results = r.json()

    # bogger

    # # trip_option is a list of dictionaries, one dictionary per option. 

    # departure_date = trip_options[0]["slice"][0]["segment"][0]["leg"][0]["departureTime"]
    # airport_code_departure = search_results["trips"]["data"]["city"][0]["code"]
    # airport_name_departure = search_results["trips"]["data"]["city"][0]["name"]

    # arrival_date = trip_options[0]["slice"][0]["segment"][0]["leg"][0]["arrivalTime"]
    # airport_code_arrival = search_results["trips"]["data"]["city"][1]["code"]
    # airport_name_arrival = search_results["trips"]["data"]["city"][1]["name"]

    # aircraft_name = search_results["trips"]["data"]["aircraft"][0]["name"]
    # carrier_code = search_results["trips"]["data"]["carrier"][0]["code"]
    # carrier_name = search_results["trips"]["data"]["carrier"][0]["name"]
    # flight_duration = search_results["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["duration"]

    # # airfare_total = search_results["trips"]["tripOption"][0]["saleTotal"]
    # sale_fare_total = trip_options[0]["pricing"][0]["saleFareTotal"]
    # sale_tax_total = strip_options[0]["pricing"][0]["saleTaxTotal"]
    # sale_total = trip_options[0]["pricing"][0]["saleTotal"]


    trip_options = search_results["trips"]["tripOption"] 
    flight_duration = trip_options[0]["slice"][0]["segment"][0]["leg"][0]["duration"]
    sale_total = trip_options[0]["saleTotal"]

    r = json.dumps(search_results)
    print r



    return render_template("airfares.html", departure_date=departure_date,
                           airport_code_departure=airport_code_departure,
                           airport_name_departure=airport_name_departure,
                           arrival_date=arrival_date,
                           airport_code_arrival=airport_code_arrival,
                           airport_name_arrival=airport_name_arrival,
                           aircraft_name=aircraft_name,
                           carrier_code=carrier_code,
                           carrier_name=carrier_name,
                           flight_duration=flight_duration,
                           sale_fare_total=sale_fare_total,
                           sale_tax_total=sale_tax_total,
                           sale_total=sale_total)


################

# departure_date
# airport_code_departure
# airport_name_departure

# arrival_date
# airport_code_arrival
# airport_name_arrival

# carrier_code
# carrier_name
# flight_duration is in minutes

# ###airfare_total
# sale_fare_total
# sale_tax_total
# sale_total


# num_free_baggagge = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["pieces"]
# free_baggage_weigh = search_results["trips"]["tripOption"][0]["pricing"][0]["segmentPricing"][0]["freeBaggageOption"][0]["kilosPerPieces"]

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
