import os
from dotenv import load_dotenv
from oura_ring import OuraClient
import pandas as pd
from datetime import date, timedelta

# start date = today - 7 days, end date = today, in YYYY-MM-DD format
start_date = date.today() - timedelta(days=30)
end_date = date.today()
start_date = start_date.strftime('%Y-%m-%d')
end_date = end_date.strftime('%Y-%m-%d')

load_dotenv()

def create_oura_client(api_key):
    return OuraClient(api_key)

def validate_api_keys(api_key1, api_key2):
    try:
        client1 = create_oura_client(api_key1)
        client2 = create_oura_client(api_key2)
        client1.get_personal_info()  # Test the API key
        client2.get_personal_info()  # Test the API key
        return True
    except:
        return False

def process_data(data):
    df = pd.DataFrame(data)
    df = df[['day', 'score']]
    # print("Processed data:", df)
    return df.to_dict(orient='records')

def get_dashboard_data(api_key1, api_key2, start_date=start_date, end_date=end_date):
    client1 = create_oura_client(api_key1)
    client2 = create_oura_client(api_key2)

    sleep_data1 = client1.get_daily_sleep(start_date, end_date)
    sleep_data2 = client2.get_daily_sleep(start_date, end_date)
    readiness_data1 = client1.get_daily_readiness(start_date, end_date)
    readiness_data2 = client2.get_daily_readiness(start_date, end_date)

    data1 = {
        'sleep': process_data(sleep_data1),
        'readiness': process_data(readiness_data1)
    }
    data2 = {
        'sleep': process_data(sleep_data2),
        'readiness': process_data(readiness_data2)
    }

    return data1, data2

