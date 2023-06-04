import requests
import logging

class AvailabilityChecker:
    """
    A class used to check the availability of iPhone models in different cities.

    ...

    Methods
    -------
    check_availability(city, zip_code, model, color)
        Returns the availability of the specified iPhone model in the specified city
    """

    def __init__(self, api_key):
        """
        Constructs all the necessary attributes for the availability checker object.

        ...

        Attributes
        ----------
        headers : dict
            User-Agent header to use for the HTTP requests
        """
        
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        self.api_key = api_key  # API key for the ZipCodeAPI

    def get_zip_code(self, city, state):
        """
        Gets the first ZIP code for the given city using the ZipCodeAPI.

        Parameters:
            city (str): The name of the city
            state (str): The two-letter state abbreviation

        Returns:
            str: The first ZIP code for the city
        """
        # Replace spaces in the city name with '+'
        city = city.replace(' ', '+')
        response = requests.get(f'https://www.zipcodeapi.com/rest/{self.api_key}/city-zips.json/{city}/{state}')
        if response.status_code != 200:
            logging.error(f"Error occurred: {response.json()['error_msg']}")
            return None
        data = response.json()
        logging.info(f"ZIP code for {city} is {data['zip_codes'][0]}")
        return data['zip_codes'][0]

    def _get_response(self, model, zip_code):
        """
        Sends a GET request to the Apple website to check the availability of a specific iPhone model.

        Parameters:
            model (str): The model code of the iPhone
            zip_code (str): The ZIP code of the city
        
        Returns:
            str: The json of the response if the request is successful, otherwise None
        """

        URL = f"https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&cppart=UNLOCKED/US&parts.0={model}&location={zip_code}"
        try:
            r = requests.get(URL, headers=self.headers)
            r.raise_for_status()
        except (requests.exceptions.HTTPError, 
                requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout, 
                requests.exceptions.RequestException) as err:
            logging.error(f"Error occurred: {err}")
            return None
        return r.json()

    def check_availability(self, city, zip_code, model, color):
        """
        Checks and prints the availability of a specific iPhone model in a specific city.

        Parameters:
            city (str): The name of the city
            zip_code (str): The ZIP code of the city
            model (str): The model code of the iPhone
            color (str): The color of the iPhone
        
        Returns:
            list: A list containing the city, color, model, store name, and availability if the iPhone is available, otherwise None
        """
        
        response = self._get_response(model, zip_code)
        if not response:
            return None

        apple_stores = response['body']['content']['pickupMessage']['stores']
        logging.info(f"Checking availability for {color} {model} in {city}...")
        available = []
        for store in apple_stores:
            logging.info(f"Checking {store['storeName']}...")
            if "Available" in store['partsAvailability'][model]['pickupSearchQuote']:
                logging.info(f"Availability found for {color} {model} in {city} - {store['storeName']}")
                # Instead of returning the very first store. Get all the stores that have the iPhone available.
                available.append([city, color, model, store['storeName'], store['partsAvailability'][model]['pickupSearchQuote']])
        if available:
            return available

        logging.info(f"N/A in {city} for {color} {model}")
        return None
