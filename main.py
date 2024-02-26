import pandas as pd
from api_data_treatment import treat_data

from get_data_for_years import fetch_and_save_consumption_data
from get_tempo_data import fetch_and_save_tempo_data
from datetime import datetime

# def filter_last_day_of_month(df):
#     # Convert 'date' column to datetime with dayfirst=True
#     df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    
#     # Extract year and month to group by
#     df['year_month'] = df['date'].dt.to_period('M')
    
#     # Find the last day of each month
#     last_day_of_month = df.groupby('year_month')['date'].max().reset_index()
    
#     # Merge with the original DataFrame to get the corresponding rows
#     result_df = pd.merge(last_day_of_month, df, on=['year_month', 'date'], how='left')
    
#     # Drop the additional 'year_month' column
#     result_df = result_df.drop(columns=['year_month'])
    
#     return result_df

# # Read the CSV file
# input_file = 'mes-index-elec-004025197798-54000.csv'  # Replace with your actual input file name
# output_file = 'output_file.csv'  # Replace with your desired output file name

# df = pd.read_csv(input_file, sep=';')

# # Filter and create a new DataFrame with only the last day of each month
# result_df = filter_last_day_of_month(df)

# # Save the result to a new CSV file
# result_df.to_csv(output_file, index=False)

def init_data(year):
    try:
        fetch_and_save_tempo_data(year)
        fetch_and_save_consumption_data(year)
    except Exception as e:
        raise Exception(f"Failed to fetch data for {year}. Error: {e}")

current_year = datetime.now().year
for year in range(2022, current_year + 1):
    try :
        init_data(year)
        treat_data(year)
    except Exception as e:
        print(e)
        print("Error while fetching data")
