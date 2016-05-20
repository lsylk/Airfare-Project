from processing_data import request_user_input, find_one_way_flights, find_cheap_airfare_by_case, currencyadd

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from pprint import pprint

# with open("sample_5.json") as json_file:
#     json_data = json.load(json_file)

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRETKEYSECRET"

# Raises an error if an undefined variable in Jinja2 fails silently.
app.jinja_env.undefined = StrictUndefined

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         Custom Filters for Jinja
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
app.jinja_env.filters['currencyadd'] = currencyadd


@app.route('/')
def search():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/results', methods=["POST"])
def get_airfares():
    """Gets the cheapest airfares based on users input."""

    cheap_airfares = find_cheap_airfare_by_case()  # calls the function to get the results based on the type of trip (i.e. one-way, roundtrip, multicity).

    parsed_results = cheap_airfares[0]

    parsed_results_return = cheap_airfares[1]

    return render_template("airfares.html",
                           parsed_results=parsed_results,
                           parsed_results_return=parsed_results_return)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
