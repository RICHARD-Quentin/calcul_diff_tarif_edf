import json
import requests
import os
import dotenv
from datetime import datetime, timedelta
import pytz
import urllib.parse

# Create the directory if it doesn't exist
folder_name = "api_data"
os.makedirs(folder_name, exist_ok=True)

dotenv.load_dotenv()
bearer = os.getenv("BEARER")
person_ext_id = os.getenv("PERSON_EXT_ID")

# Headers based on the cURL command
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "authority": "equilibre.edf.fr",
    "authorization": f"Bearer {bearer}",  # Example token, replace with actual token
    "person-ext-id": person_ext_id,  # Example ID, replace with actual ID
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "site-ext-id": "004025197798",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

params = {
    "stepUnit": "HOURS",
    "stepValue": "1",
    "withEstimated": "SURROUNDING_ESTIMATED",
}

# Cookies parsed from the cURL command
# cookies = {
#     "9fa3e6ca36ada274b2f9b5bebeb44468": "4f9d8058a222af196467e3a57f7e08a9",
#     "_abck": "EEF67C435ECE6D11EADC826A288236B7~-1~YAAQreIlF8XHJSuMAQAANfp0Lw..."
#     # Add other cookies as needed
# }

def is_dst_cet(date):
    """
    Determines if a given date is within the Daylight Saving Time (DST) period for the CET timezone.
    
    :param date: A datetime.date object representing the date to check.
    :return: True if the date is within DST period, False otherwise.
    """
    timezone = pytz.timezone('Europe/Paris')  # 'Europe/Paris' represents CET/CEST.
    tz_date = timezone.localize(datetime(date.year, date.month, date.day, 12))  # Noon to avoid any day change issues.
    return tz_date.dst() != timedelta(0)

def get_cet_offset(date):
    """
    Returns the string representation of the CET time offset (+01:00 or +02:00) based on DST.
    
    :param date: A datetime.date object representing the date to check.
    :return: A string representing the CET time offset.
    """
    return "+02:00" if is_dst_cet(date) else "+01:00"

def fetch_and_save_consumption_data(year):
    data = []
    sorted_data = {}
    # Loop over each month from January to December
    for month in range(1, 13):
        # Adjust these dates based on the year and month
        offset = get_cet_offset(datetime(year, month, 1))
        start_month = str(month).zfill(2)
        begin_ts = f"{year}-{start_month}-01T00:00:00.000{offset}"

        end_month = "01" if month == 12 else str(month + 1).zfill(2)
        end_year = year if month != 12 else year + 1
        end_ts = f"{end_year}-{end_month}-01T00:00:00.000{offset}"

        url_params = urllib.parse.urlencode({
            "beginTs": begin_ts,
            "endTs": end_ts,
            "stepUnit": "HOURS",
            "stepValue": "1",
            "withEstimated": "SURROUNDING_ESTIMATED",
        })

        url = f"https://equilibre.edf.fr/api/v2/sites/-/consumptions?{url_params}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            consumption = response.json().get("consumptions")
            data += consumption
        else:
            print(url)
            raise Exception(f"Failed to fetch data for {year}. Status code: {response.status_code}")
        
    # Sort the data by date
    for period in data:
        [day, time] = period.get("period").get("startTime").split("T")
        if day not in sorted_data:
            sorted_data[day] = {
                "consumption": 0,
                "cost": 0,
                "hp_hc": {
                    "HP": 0,
                    "HC": 0,
                },
                "tempo": {
                    "HP": 0,
                    "HC": 0,
                },
            }

        hour = int(time.split(":")[0])
        consumption = period.get("energyMeter").get("total")
        cost = period.get("cost").get("total")

        sorted_data[day]["hp_hc"]["HC" if hour in range(0, 8) or hour in range(12, 14) else "HP"] += consumption
        sorted_data[day]["tempo"]["HC" if hour in range(0, 8) or hour in range(22, 24) else "HP"] += consumption
        sorted_data[day]["consumption"] += consumption
        sorted_data[day]["cost"] += cost

        # Write the response to a file named with the year and month in the 'api_data' folder
    with open(os.path.join(folder_name, f"{year}.json"), 'w', encoding='utf-8') as file:
        file.write(json.dumps(sorted_data, indent=4))
    print(f"Consumption data for {year} saved successfully.")

# def fetch_and_save_consumption_data(year):
#     # Adjust these dates for the desired year
#     print(f"Fetching consumption data for {year}...")
#     # print(f"Headers: {headers}")
#     begin_ts = f"{year}-01-01T23:00:00.000Z"
#     end_ts = f"{year}-12-31T23:00:00.000Z"
    
#     url = f"https://equilibre.edf.fr/api/v2/sites/-/consumptions?beginTs={begin_ts}&endTs={end_ts}&stepUnit=HOURS&stepValue=1&withEstimated=SURROUNDING_ESTIMATED"
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         # Write the response to a file named with the year in the 'api_data' folder
#         with open(os.path.join(folder_name, f"{year}.json"), 'w', encoding='utf-8') as file:
#             file.write(response.text)
#         print(f"Consumption data for {year} saved successfully.")
#     else:
#         raise Exception(f"Failed to fetch data for {year}. Status code: {response.status_code}")

# def fetch_all_consumption_data():
#     # Loop over each year from 2022 to the current year
#     current_year = datetime.now().year
#     for year in range(2022, current_year + 1):
#         fetch_and_save_data(year)
