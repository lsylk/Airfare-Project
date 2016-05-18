from unittest import TestCase

from server import app


class RequestTests(TestCase):
    """Tests for my Cheapest Flights site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Welcome to Flights", result.data)

    def test_no_user_input_yet(self):
        result = self.client.get("/")
        self.assertIn("Please insert the values", result.data)
        self.assertNotIn("Cheapest Flights", result.data)

    def test_with_user_input(self):
        """Test user input."""

        result = self.client.post("/results",
                                  data={"departure": 'LAX',
                                        "arrival": 'SFO',
                                        "departure-date": '2016-09-10',
                                        "arrival-date": '2016-11-10',
                                        "results": '2'},
                                  follow_redirects=False)
        self.assertIn("Cheapest Flights", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()
    # print
    # result = unittest.result()
    # if result.wasSuccessful():
    #     print "ALL TESTS PASSED!"
    # print
