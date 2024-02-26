import requests
import os
from datetime import datetime, timedelta

# Create the directory if it doesn't exist
folder_name = "tempo"
os.makedirs(folder_name, exist_ok=True)

# Headers based on the cURL command
headers = {
    "authority": "api-commerce.edf.fr",
    "accept": "application/json, text/plain, */*",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "application-origine-controlee": "site_RC",
    "content-type": "application/json",
    "origin": "https://particulier.edf.fr",
    "referer": "https://particulier.edf.fr/",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "situation-usage": "Jours Effacement",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "x-request-id": "1708939848783",
}

def fetch_and_save_tempo_data(year):
    # Adjust these dates based on the year
    dateApplicationBorneInf = f"{year}-01-01"
    dateApplicationBorneSup = f"{year}-12-31"
    
    url = f"https://api-commerce.edf.fr/commerce/activet/v1/calendrier-jours-effacement?option=TEMPO&dateApplicationBorneInf={dateApplicationBorneInf}&dateApplicationBorneSup={dateApplicationBorneSup}&identifiantConsommateur=src"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Write the response to a file named with the year in the 'tempo' folder
        with open(os.path.join(folder_name, f"{year}.json"), 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Tempo data for {year} saved successfully.")
    else:
        raise Exception(f"Failed to fetch data for {year}. Status code: {response.status_code}")

# def fetch_all_tempo_data():
#     # Loop over each year from 2022 to the current year
#     current_year = datetime.now().year
#     for year in range(2022, current_year + 1):
#         fetch_and_save_data(year)

