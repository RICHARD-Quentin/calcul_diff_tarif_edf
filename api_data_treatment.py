import json
import csv
from typing import List, Dict
from apiInterface import Consumption

# Constants
tarif_base = {
    "2022": 0.1740,
    "2023": 0.2276,
    "2024": 0.2310,
}

tarif_tempo = {
    "2022": {
        "TEMPO_BLEU": {
            "HC": 0.0862,
            "HP": 0.1272,
        },
        "TEMPO_BLANC": {
            "HC": 0.1112,
            "HP": 0.1653,
        },
        "TEMPO_ROUGE": {
            "HC": 0.1222,
            "HP": 0.5486,
        },
    },
    "2023": {
        "TEMPO_BLEU": {
            "HC": 0.0970,
            "HP": 0.1249,
        },
        "TEMPO_BLANC": {
            "HC": 0.1140,
            "HP": 0.1508,
        },
        "TEMPO_ROUGE": {
            "HC": 0.1216,
            "HP": 0.6712,
        },
    },
    "2024": {
        "TEMPO_BLEU": {
            "HC": 0.1296,
            "HP": 0.1609,
        },
        "TEMPO_BLANC": {
            "HC": 0.1486,
            "HP": 0.1894,
        },
        "TEMPO_ROUGE": {
            "HC": 0.1568,
            "HP": 0.7562,
        },
    }
}

tarif_abonnement = {
    "BASE": 15.79,
    "HP/HC": 16.70,
    "TEMPO": 16.16,
}

jours_tempo = {}

def read_json_file(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def format_decimal(value: float) -> str:
    formatted_value = f"{value:.2f}"  # Format to two decimal places
    return formatted_value.replace('.', ',')

def format_jours_tempo(year) -> List[str]:
    days = []
    # json_files = os.listdir('./tempo')
    # for file in json_files:
    json_data = read_json_file('./tempo/' + str(year) + '.json')
    
    options = json_data.get('content', {}).get('options', [])
    days = options[0].get('calendrier', [])
    for day in days:
        jours_tempo[day['dateApplication']] = day['statut']


def get_tempo_color_by_date(date: str) -> str:
    return jours_tempo[date]

def get_tarif_tempo(date: str, conso_hp: float, conso_hc: float) -> Dict:
    color = get_tempo_color_by_date(date)
    year = date.split('-')[0]
    try:
        return {
            "Conso HP": format_decimal(conso_hp * tarif_tempo[year][color]['HP']),
            "Conso HC": format_decimal(conso_hc * tarif_tempo[year][color]['HC']),
            "Conso Total": format_decimal(conso_hp * tarif_tempo[year][color]['HP'] + conso_hc * tarif_tempo[year][color]['HC']),
        }
    except:
        print("Error while processing tempo")
        return {
            "Conso HP": 0,
            "Conso HC": 0,
            "Conso Total": 0,
        }

def process_consumptions(consumptions: List[Consumption], tarif_base: float) -> List[Dict]:
    processed_data = []
    errors = []
    for consumption in consumptions:
        try:
            date = consumption['period']['startTime'].split('T')[0]
            dateFormated = date.split('-')[2] + '/' + date.split('-')[1] + '/' + date.split('-')[0]
            total_energy = consumption['energyMeter']['total']
            conso_hp = consumption['energyMeter']['byTariffHeading']['HP']
            conso_hc = consumption['energyMeter']['byTariffHeading']['HC']
            total_cost = format_decimal(consumption['cost']['total'] - consumption['cost']['standingCharge'])
            cost_hp = format_decimal(consumption['cost']['byTariffHeading']['HP'])
            cost_hc = format_decimal(consumption['cost']['byTariffHeading']['HC'])
            additional_value = format_decimal(total_energy * tarif_base)
            tempo = get_tarif_tempo(date, conso_hp, conso_hc)

            processed_data.append({
                "Date": dateFormated,
                "Consomation (kwh)": total_energy,
                "Conso HP": conso_hp,
                "Conso HC": conso_hc,
                "Cout HP": cost_hp,
                "Cout HC": cost_hc,
                "Cout total (€)": total_cost,
                "Cout tarif base": additional_value,
                "Cout tarif tempo total": tempo['Conso Total'],
                "Cout tarif tempo HP": tempo['Conso HP'],
                "Cout tarif tempo HC": tempo['Conso HC'],
            })
        except Exception as e:
            errors.append(f"Error while processing consumption for {consumption['period']['startTime']} : {e}")
    
    if len(errors) > 0:    
        print(f"Error while processing consumption for {len(errors)} dates")

    return processed_data

def write_to_csv(data: List[Dict], file_path: str):
    total_cout_total = 0
    total_cout_base = 0
    total_cout_tempo = 0

    with open(file_path, 'w', newline='') as file:
        print("Writing to file: " + file_path + "...")
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=';')
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            total_cout_total += float(row['Cout total (€)'].replace(',', '.'))
            total_cout_base += float(row['Cout tarif base'].replace(',', '.'))
            total_cout_tempo += float(row['Cout tarif tempo total'].replace(',', '.'))

        total_cout_total_str = format_decimal(total_cout_total)
        total_cout_tarif_base_str = format_decimal(total_cout_base)
        total_cout_tarif_tempo_total_str = format_decimal(total_cout_tempo)

        # Write the totals row
        writer.writerow({
            "Date": "Total",
            "Consomation (kwh)": "",
            "Conso HP": "",
            "Conso HC": "",
            "Cout HP": "",
            "Cout HC": "",
            "Cout total (€)": total_cout_total_str,
            "Cout tarif base": total_cout_tarif_base_str,
            "Cout tarif tempo total": total_cout_tarif_tempo_total_str,
            "Cout tarif tempo HP": "",
            "Cout tarif tempo HC": "",
        })

        last_row = data[-1]
        last_month = int(last_row['Date'].split('/')[1])

        
        total_avec_abonement = total_cout_total + 16.70*last_month
        total_avec_abonement_base = total_cout_base + 15.79*last_month
        total_avec_abonement_tempo = total_cout_tempo + 16.16*last_month

        total_avec_abonement_str = format_decimal(total_avec_abonement)
        total_avec_abonement_base_str = format_decimal(total_avec_abonement_base)
        total_avec_abonement_tempo_str = format_decimal(total_avec_abonement_tempo)

        # Write the totals row
        writer.writerow({
            "Date": "Total avec abonement",
            "Consomation (kwh)": "",
            "Conso HP": "",
            "Conso HC": "",
            "Cout HP": "",
            "Cout HC": "",
            "Cout total (€)": total_avec_abonement_str,
            "Cout tarif base": total_avec_abonement_base_str,
            "Cout tarif tempo total": total_avec_abonement_tempo_str,
            "Cout tarif tempo HP": "",
            "Cout tarif tempo HC": "",
        })
    
    print("File written successfully.")


# Main script execution
#Fetch all tempo data
# fetch_all_consumption_data()
# fetch_all_tempo_data()
def treat_data(year):
    format_jours_tempo(year)
    # for file in json_files:
    json_data = read_json_file('./api_data/' + str(year) + '.json')
    consumptions = json_data.get('consumptions', [])
    tarif = tarif_base.get(str(year), 0)
    processed_data = process_consumptions(consumptions, tarif)
    write_to_csv(processed_data, './api_results/' + str(year) + '.csv')
