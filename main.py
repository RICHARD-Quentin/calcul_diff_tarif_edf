import os
from api_data_treatment import treat_data
from get_data_for_years import fetch_and_save_consumption_data
from get_tempo_data import fetch_and_save_tempo_data
from datetime import datetime

def init_data(year):
    try:
        fetch_and_save_tempo_data(year)
        fetch_and_save_consumption_data(year)
    except Exception as e:
        raise Exception(f"Failed to fetch data for {year}. Error: {e}")
    

# Create the directory if it doesn't exist
print("Creating directories...")
os.makedirs("tempo", exist_ok=True)
os.makedirs("api_data", exist_ok=True)
os.makedirs("api_results", exist_ok=True)

#Check if .env file is set
print("Checking Bearer token...")
if os.getenv("BEARER") is None:
    raise Exception("BEARER token is not set")

print("Checking Person Ext ID...")
if os.getenv("PERSON_EXT_ID") is None:
    raise Exception("PERSON_EXT_ID is not set")

current_year = datetime.now().year
for year in range(2022, current_year + 1):
    try :
        init_data(year)
        treat_data(year)
    except Exception as e:
        print(e)
        print("Error while fetching data")