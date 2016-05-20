from unittest import TestCase

from server import app


class RequestTests(TestCase):
    """Tests for my Cheapest Flights site."""

    def setUp(self):
        """This function is set up at the beginning of each TestCase."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test that the homepage is rendered."""

        result = self.client.get("/")
        self.assertIn("Welcome to Flights", result.data)

    def test_no_user_input_yet(self):
        """Test hompage when user has not input values yet."""

        result = self.client.get("/")
        self.assertIn("Please insert the values", result.data)
        self.assertNotIn("Cheapest Flights", result.data)

    def test_with_user_input_oneWay(self):
        """Test user input to find one-way trip."""

        result = self.client.post("/results",
                                  data={"departure": 'LAX',
                                        "arrival": 'SFO',
                                        "departure-date": '2016-09-10',
                                        "return-date": '',
                                        "results": '2'},
                                  follow_redirects=False)
        self.assertIn("Cheapest Flights", result.data)
        self.assertNotIn("Returning", result.data)

    def test_with_user_input_round_trip(self):
        """Test user input to find round trip."""

        result = self.client.post("/results",
                                  data={"departure": 'LAX',
                                        "arrival": 'SFO',
                                        "departure-date": '2016-09-10',
                                        "return-date": '2016-11-10',
                                        "results": '2'},
                                  follow_redirects=False)
        self.assertIn("Cheapest Flights", result.data)
        self.assertIn("Returning", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
