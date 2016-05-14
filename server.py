from processing_data import request_user_input, search_flights, processing_data, instantiate_datetime_object, format_datetime_object

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from pprint import pprint

# with open("sample_5.json") as json_file:
#     json_data = json.load(json_file)

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
def get_airfares():

    request_inputs = request_user_input()

    search_flights_json = search_flights(request_inputs)

    processing_data_results = processing_data(search_flights_json, request_inputs)

    return render_template("airfares.html",
                           processing_data_results=processing_data_results)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()





    # {% for result in processing_data_results %}
    #         <li> Departure date: {{ result[0] }} at {{ result[1] }}</li>
    #         <li> Departing from {{ result[2] }}: {{ result[3] }}</li>
    #         <li> Arrival date {{ result[4] }} at {{ result[5] }}</li>
    #         <li> Arriving to {{ result[6] }}: {{ result[7] }}</li>
           
    #         <li> Airlines : {{ result[8] }} {{ result[9] }} - {{ result[10] }} </li>
          
    #         <li> Flight duration: {{ result[11] }} minutes</li>
    #         <li> Airfare: {{ result[12] }}</li>
    #         <li> Tax: {{ result[13] }}</li>
    #         <li> Total: {{ result[14] }}</li>
           
    #         <br></br>

    #         {% endfor %}
