import urllib2
import json

origin = raw_input("Origin of destination ").upper()
destination = raw_input("Final destination ").upper()
departure_day = raw_input("Departure day (yyyy-mm-day) ")
adult_passengers = raw_input("How many adults are traveling? ")
number_of_options = raw_input("How many options do you want? ")

# HTTP request
request_url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=XXXX"


# Structure of the request body

############### Commented varibles might be used to add new features.
request_body = {
    "request": {
        "passengers": {
            "kind": "qpxexpress#passengerCounts",
            "adultCount": int(adult_passengers),
            # "childCount": integer,
            # "infantInLapCount": integer,
            # "infantInSeatCount": integer,
            # "seniorCount": integer
        },
        "slice": [
            {
                "kind": "qpxexpress#sliceInput",
                "origin": origin,
                "destination": destination,
                "date": departure_day,
                # "maxStops": integer,
                # "maxConnectionDuration": integer,
                # "preferredCabin": string,
                # "permittedDepartureTime": {
                #     "kind": "qpxexpress#timeOfDayRange",
                #     "earliestTime": string,
                #     "latestTime": string
                # },
                # "permittedCarrier": [
                #     string
                # ],
                # "alliance": string,
                # "prohibitedCarrier": [
                #     string
                # ]
            }
        ],
        # "maxPrice": string,
        # "saleCountry": string,
        # "refundable": boolean,
        "solutions": int(number_of_options)
    }
}

# Dump is data taken from a storage medium.
# UTF-8 is a character encoding capable of encoding all possible characters, or code points, defined by Unicode. The encoding is variable-length and uses 8-bit code units.
# Takes the data from Google's  Airfare database
json_request_body = json.dumps(request_body, enconding='utf-8')

# Abstracting from request_url
user_request = urllib2.Request(request_url, json_request_body, {'Content-Type': 'application/json'})
