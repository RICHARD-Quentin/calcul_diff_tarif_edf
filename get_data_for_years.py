import requests
import os
import dotenv

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

# Cookies parsed from the cURL command
# cookies = {
#     "9fa3e6ca36ada274b2f9b5bebeb44468": "4f9d8058a222af196467e3a57f7e08a9",
#     "_abck": "EEF67C435ECE6D11EADC826A288236B7~-1~YAAQreIlF8XHJSuMAQAANfp0Lw..."
#     # Add other cookies as needed
# }

def fetch_and_save_consumption_data(year):
    # Adjust these dates for the desired year
    print(f"Fetching consumption data for {year}...")
    # print(f"Headers: {headers}")
    begin_ts = f"{year}-01-01T23:00:00.000Z"
    end_ts = f"{year}-12-31T23:00:00.000Z"
    
    url = f"https://equilibre.edf.fr/api/v2/sites/-/consumptions?beginTs={begin_ts}&endTs={end_ts}&stepUnit=DAYS&stepValue=1&withEstimated=SURROUNDING_ESTIMATED"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Write the response to a file named with the year in the 'api_data' folder
        with open(os.path.join(folder_name, f"{year}.json"), 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Consumption data for {year} saved successfully.")
    else:
        raise Exception(f"Failed to fetch data for {year}. Status code: {response.status_code}")

# def fetch_all_consumption_data():
#     # Loop over each year from 2022 to the current year
#     current_year = datetime.now().year
#     for year in range(2022, current_year + 1):
#         fetch_and_save_data(year)
