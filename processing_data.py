from os import environ

import requests

import json

from datetime import datetime


def get_carrier_name(cheap_airfares):
    "Parse carrier's name and creates a list."

    num = range(len(cheap_airfares))

    carrier_names = []

    if cheap_airfares[1] is None:
        carrier_name = cheap_airfares[0][0]['carrier_name']
        carrier_name = carrier_name.split(' ')
        carrier_names.append(carrier_name)

    else:
        for n in num:
            for flight in cheap_airfares:
                carrier_name = cheap_airfares[n][0]['carrier_name']
                carrier_name = carrier_name.replace(',', ' ')
                carrier_name = carrier_name.split(' ')
                carrier_names.append(carrier_name)
                break
        print carrier_names

    # num = range(len(cheap_airfares))

    # if cheap_airfares[1] is None:
    #     carrier_name = cheap_airfares[0]['carrier_name']
    #     carrier_name = carrier_name.split(' ')

    # else:
    #     for n in num:
    #         for flight in cheap_airfares:
    #             carrier_name = cheap_airfares[n][0]['carrier_name']
    #             carrier_name = carrier_name.split(' ')
    #             break

    # cheap_airfares = [[{'carrier_name': u'Virgin America Inc.'}], [{'carrier_name': u'Frontier Airlines, Inc.'}], [{'carrier_name': u'Alaska Airlines Inc.'}]]

    # cheap_airfares from server
# #################################################
# [([{'sale_total': u'USD313.10', 'departure_date': 'Sunday, 05 June 2016', 'airport_name_arrival': u'Miami', 'sale_fare_total': u'USD278.14', 'arrival_time': '07:07PM', 'airport_name_departure': u'Los Angeles', 'carrier_name': u'Alaska Airlines Inc.', 'airport_code_departure': u'LAX', 'flight_duration': 307, 'departure_time': '11:00AM', 'arrival_date': 'Sunday, 05 June 2016', 'airport_code_arrival': u'MIA', 'sale_tax_total': u'USD34.96', 'carrier_code': u'AS', 'aircraft_number': u'1174'}], u'alaskaairlines.com'), ([{'sale_total': u'USD734.10', 'departure_date': 'Thursday, 16 June 2016', 'airport_name_arrival': u'San Diego', 'sale_fare_total': u'USD669.76', 'arrival_time': '10:05PM', 'airport_name_departure': u'Miami', 'carrier_name': u'Alaska Airlines Inc.', 'airport_code_departure': u'MIA', 'flight_duration': 304, 'departure_time': '08:01PM', 'arrival_date': 'Thursday, 16 June 2016', 'airport_code_arrival': u'SAN', 'sale_tax_total': u'USD64.34', 'carrier_code': u'AS', 'aircraft_number': u'1998'}], u'alaskaairlines.com')]
# #################################################
#GooooooD##########
    # num = range(len(cheap_airfares))

    # carrier_names = []

    # for n in num:
    #     for flight in cheap_airfares:
    #         carrier_name = cheap_airfares[n][0]['carrier_name']
    #         carrier_name = carrier_name.replace(',', ' ')
    #         carrier_name = carrier_name.split(' ')
    #         carrier_names.append(carrier_name)
    #         break
    # print carrier_names
    # return carrier_names


def make_airline_link(carrier_names):
    """Creates a string for an airline's website."""

    airlines = []

    for carrier_name in carrier_names:
        carrier_name = carrier_name[:2]
        airline_link = ""
        for word in carrier_name:
            airline_link = airline_link + word

        airlines.append(airline_link)

    airline_links = []

    for airline in airlines:
        airline_link = (airline+".com").lower()
        airline_links.append(airline_link)

    return airline_links


def sum_of_sale_total_multicity(cheap_airfares):
    """Calculates the Total for the mulcity search."""

    num = range(len(cheap_airfares))

    Total = 0
    for n in num:
        for flight in cheap_airfares:
            sale_total = float(cheap_airfares[n][0]['sale_total'][3:])
            Total = round(Total + sale_total, 2)
            break

    return Total


def find_one_way_flights(request_inputs):
    """Finds one-way flights."""

    search_flights_json = search_flights(request_inputs)

    processing_data_results = parsing_data(search_flights_json, request_inputs)

    return processing_data_results


def find_multicity_flights(multicity_requests):
    """Finds multi-city flights."""

    search_flights_json = map(search_flights, multicity_requests)

    processing_data_results = map(parsing_data, search_flights_json, multicity_requests)

    #  returns a list of list of dictionaries: i.e. [
    #[{'sale_total': u'USD223.10', 'departure_date': 'Monday, 30 May 2016', 'airport_name_arrival': u'San Francisco', 'sale_fare_total': u'USD194.42', 'arrival_time': '11:52PM', 'airport_name_departure': u'Los Angeles', 'carrier_name': u'United Airlines, Inc.', 'airport_code_departure': u'LAX', 'flight_duration': 86, 'departure_time': '10:26PM', 'arrival_date': 'Monday, 30 May 2016', 'airport_code_arrival': u'SFO', 'sale_tax_total': u'USD28.68', 'carrier_code': u'UA', 'aircraft_number': u'398'}],

    #[{'sale_total': u'USD374.25', 'departure_date': 'Saturday, 25 June 2016', 'airport_name_arrival': u'San Francisco', 'sale_fare_total': u'USD335.02', 'arrival_time': '04:54PM', 'airport_name_departure': u'Miami', 'carrier_name': u'Alaska Airlines Inc.', 'airport_code_departure': u'MIA', 'flight_duration': 339, 'departure_time': '08:15AM', 'arrival_date': 'Saturday, 25 June 2016', 'airport_code_arrival': u'SFO', 'sale_tax_total': u'USD39.23', 'carrier_code': u'AS', 'aircraft_number': u'1060'}]
    #]

    parsed_results = processing_data_results

    return parsed_results


def find_cheap_airfare_by_case(request_inputs):
    """Gets the cheapest airfares based on users input."""

    return_date = request_inputs['return_date']

    # case: one-way
    if return_date == '':
        parsed_results = find_one_way_flights(request_inputs)
        parsed_results_return = None

        cheap_airfares = (parsed_results, parsed_results_return)

    # case: roundtrip
    else:
        parsed_results = find_one_way_flights(request_inputs)

        return_flights = {'departure': request_inputs['arrival'],
                          'arrival': request_inputs['departure'],
                          'departure_date': request_inputs['return_date'],
                          'number_of_results': request_inputs['number_of_results']}

        parsed_results_return = zip(parsed_results, find_one_way_flights(return_flights))

        cheap_airfares = (parsed_results, parsed_results_return)

    return cheap_airfares


def create_dict_with_multicity_inputs(multicity_results):
    """Creates a dictionary based on user's input."""

    multicity_dict = {'departure': multicity_results[0],
                      'arrival': multicity_results[1],
                      'departure_date': multicity_results[2],
                      'number_of_results': multicity_results[3]}

    return multicity_dict


def instantiate_datetime_object(datetime_stamps):
    """Takes a datestamp as a string and instatiates it into an object.

    >>> datetime_stamps = [u'2016-09-10T15:35-07:00', u'2016-09-10T16:48-07:00']
    >>> instantiate_datetime_object(datetime_stamps)
    [datetime.datetime(2016, 9, 10, 15, 35, 7), datetime.datetime(2016, 9, 10, 16, 48, 7)]

    >>> datetime_stamps = [u'2016-09-10T15:35-07:00']
    >>> instantiate_datetime_object(datetime_stamps)
    [datetime.datetime(2016, 9, 10, 15, 35, 7)]

    """

    all_datetime_stamps = []

    parse_date_format1 = "%Y-%m-%dT%H:%M+%S:%f"
    parse_date_format2 = "%Y-%m-%dT%H:%M-%S:%f"

    for datetime_stamp in datetime_stamps:
        if "+" in datetime_stamp:
            datetime_object = datetime.strptime(datetime_stamp, parse_date_format1)
            all_datetime_stamps.append(datetime_object)
        else:
            datetime_object = datetime.strptime(datetime_stamp, parse_date_format2)
            all_datetime_stamps.append(datetime_object)

    return all_datetime_stamps  # returns a list of datetime objects (i.e.[datetime.datetime(2016, 9, 10, 15, 35, 7), datetime.datetime(2016, 9, 10, 16, 48, 7)])


def format_datetime_object(datetime_stamps):
    """Takes a datetime object and returns date and time as a string that have been formatted.

    >>> datetime_stamps = [datetime(2016, 9, 10, 15, 35, 7), datetime(2016, 9, 10, 16, 48, 7)]
    >>> format_datetime_object(datetime_stamps)
    [('Saturday, 10 September 2016', '03:35PM'), ('Saturday, 10 September 2016', '04:48PM')]

    >>> datetime_stamps = [datetime(2016, 9, 10, 15, 35, 7)]
    >>> format_datetime_object(datetime_stamps)
    [('Saturday, 10 September 2016', '03:35PM')]

    """

    all_date_time_stamps = []

    for datetime_object in datetime_stamps:
        date_stamp = datetime_object.strftime("%A, %d %B %Y")
        time_stamp = datetime_object.strftime("%I:%M%p")
        all_date_time_stamps.append((date_stamp, time_stamp))

    return all_date_time_stamps  # returns a list of tupples (i.e. [('Saturday, 10 September 2016', '03:35PM'), ('Saturday, 10 September 2016', '04:48PM')])


def search_flights(request_inputs):
    """Makes an API call and searches for flights based on user's input information."""

    API_KEY = environ['AIRFARE_USER_KEY']

    # HTTP request to google's QPX API
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
                    "origin": str(request_inputs['departure']),
                    "destination": str(request_inputs['arrival']),
                    "date": str(request_inputs['departure_date']),
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
            "solutions": int(request_inputs['number_of_results']),
            }
        }

    # Dump is data taken from a storage medium.
    # UTF-8 is a character encoding capable of encoding all possible characters, or code points, defined by Unicode. The encoding is variable-length and uses 8-bit code units.

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    headers = {"Content-Type": "application/json"}

    request_as_json = requests.post(REQUEST_URL, data=json.dumps(payload), headers=headers)  # Used post method request and json.dumps to turn the dictionary into a JSON string

    search_results = request_as_json.json()

    # r = json.dumps(search_results)

    return search_results


def parsing_data(search_flights_json, request_inputs):
    """Parses the results from the user's search, reading it"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The values from these variables remain the same; therefore don't need to include them in the for loop.

    cities = search_flights_json["trips"]["data"]["city"]  # returns list (i.e. [{u'kind': u'qpxexpress#cityData', u'code': u'LAX', u'name': u'Los Angeles'}, {u'kind': u'qpxexpress#cityData', u'code': u'SFO', u'name': u'San Francisco'}])

    airport_code_departure = cities[0]["code"]  # returns a unicode str (i.e. u'LAX')
    airport_name_departure = cities[0]["name"]  # returns a unicode str (i.e. u'Los Angeles')
    airport_code_arrival = cities[1]["code"]  # returns a unicode str (i.e. u'SFO')
    airport_name_arrival = cities[1]["name"]  # returns a nicode str (i.e. u'San Francisco')

    all_results = []

    # This for loop iterates through the search_flights_json that was returned from the request made by the user.

    for i in range(int(request_inputs['number_of_results'])):  # request_inputs[4] is the number of options that the user input during the search.

    # The following variables are defined to call different keys from the json returned from the post request:

        #  search_flights_json["trips"]["tripOption"] is a list of dictionaries, one dictionary per option.

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        leg_0 = search_flights_json["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"][0]  # returns a dict
        departure_date = leg_0["departureTime"]  # returns a unicode str (i.e. u'2016-09-10T14:10-07:00')
        arrival_date = leg_0["arrivalTime"]  # returns a unicode str (i.e. u'2016-09-10T15:20-07:00')

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        pricing_0 = search_flights_json["trips"]["tripOption"][i]["pricing"][0]  # returns a dict
        sale_fare_total = pricing_0["saleFareTotal"]  # returns a unicode str (i.e. u'USD49.30')
        sale_tax_total = pricing_0["saleTaxTotal"]  # returns a unicode str (i.e. u'USD17.80')
        sale_total = pricing_0["saleTotal"]  # returns a unicode str (i.e. u'USD67.10')

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        slice_0 = search_flights_json["trips"]["tripOption"][i]["slice"][0]  # returns a dict
        flight_duration = slice_0["duration"]  # the duration is in minutes and returns a str (i.e. u'70')
        aircraft_number = slice_0["segment"][0]["flight"]["number"]  # returns a unicode str (i.e. u'929')
        carrier_code = slice_0["segment"][0]["flight"]["carrier"]  # returns a unicode str (i.e. u'VX')

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        carrier_data = search_flights_json["trips"]["data"]["carrier"]  # carrier_data is a nested object inside the dict, and it is a list.
        carrier_name_code = carrier_data[0]["code"]  # returns a unicode str (i.e. u'VX')
        carrier_name = carrier_data[0]["name"]  # returns a unicode str (i.e. u'Virgin America Inc.')

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Since the carrier_data is not part of the search_flights_json["trips"]["tripOption"] - list of dictionaries, this conditional was added to match the carrier_code with its specific carrier name. See comments above for more details about carrier_data.

        if carrier_code == carrier_name_code:
            carrier_name = carrier_data[0]["name"]
        else:
            carrier_name = carrier_data[1]["name"]

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        datetime_stamps = [departure_date, arrival_date]  # returns a list of datetime stamps that are not user friendly  (i.e. [u'2016-09-10T15:35-07:00', u'2016-09-10T16:48-07:00'])

        datetime_objects = instantiate_datetime_object(datetime_stamps)  # returns a list of datetime objects (i.e.[datetime.datetime(2016, 9, 10, 15, 35, 7), datetime.datetime(2016, 9, 10, 16, 48, 7)])

        datetime_stamps = format_datetime_object(datetime_objects)  # The datetime_objects have been formated to be more user friendly. This returns a list of tuples (i.e. [('Saturday, 10 September 2016', '03:35PM'), ('Saturday, 10 September 2016', '04:48PM')])

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ User Friendly datetime stamps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        departure_date = datetime_stamps[0][0]  # returns a str (i.e. 'Saturday, 10 September 2016')
        departure_time = datetime_stamps[0][1]  # returns a str (i.e. '02:10PM')
        arrival_date = datetime_stamps[1][0]  # returns a str (i.e. 'Saturday, 10 September 2016')
        arrival_time = datetime_stamps[1][1]  # returns a str (i.e. '03:20PM')

        # results is a list of the variables that have been processed and/or formatted above. Each list represents one option.
        results = {'departure_date': departure_date,
                   'departure_time': departure_time,
                   'airport_code_departure': airport_code_departure,
                   'airport_name_departure': airport_name_departure,
                   'arrival_date': arrival_date,
                   'arrival_time': arrival_time,
                   'airport_code_arrival': airport_code_arrival,
                   'airport_name_arrival': airport_name_arrival,
                   'carrier_name': carrier_name,
                   'carrier_code': carrier_code,
                   'aircraft_number': aircraft_number,
                   'flight_duration': flight_duration,
                   'sale_fare_total': sale_fare_total,
                   'sale_tax_total': sale_tax_total,
                   'sale_total': sale_total}

        all_results.append(results)  # This is a list of dictionaries and contains all the results/options that the user requested.

    return all_results


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         Custom Filters for Jinja
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def currencyadd(value1, value2):
    """Typecasts strings into floats and adds them up."""

    return float(value1[3:]) + float(value2[3:])


##############################################################################
# Unit Test
if __name__ == "__main__":
    import doctest
    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED!"
    print
