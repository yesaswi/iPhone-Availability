# Logging configuration
import logging

import pandas as pd
from fastapi import FastAPI, HTTPException, status

from availability_checker import AvailabilityChecker
from config import API_KEY, IPHONE_MODELS
from models import CityInfo

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/availability")
async def availability_report(city_info: CityInfo):
    """
    Returns the availability report for the specified city.

    Parameters:
        city (str): The name of the city

    Returns:
        dict: The availability report for the specified city
    """
    if not city_info.city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City name is required")
    
    if not city_info.state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="State name is required")

    logging.info("Starting Availability Checker...")
    availability_checker = AvailabilityChecker(api_key=API_KEY)

    zip_code = availability_checker.get_zip_code(city_info.city, city_info.state)

    # List to store the availability report
    availability_report = []

    for color, model in IPHONE_MODELS.items():
        reports = availability_checker.check_availability(city_info.city, zip_code, model, color)
        if reports:
        # Flatten the list of reports before appending them
            for report in reports:
                availability_report.append(report)

    # Creating a DataFrame from the list
    df = pd.DataFrame(availability_report, columns=['City', 'Color', 'Model', 'StoreName', 'Availability'])

    return df.to_dict('records')
