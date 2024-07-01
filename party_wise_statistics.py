import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Create a directory to save the CSV files
os.makedirs('Party_Wise_Winning_Statistics', exist_ok=True)

# Dictionary to hold party names and their corresponding URLs
party_urls = {
    'Bhartiya_Janta_Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-369.htm',
    'Indian_National_Congress': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-742.htm',
    'Samajwadi_Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1680.htm',
    'All India Trinamool Congress': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-140.htm',
    'Dravida Munnetra Kazhagam': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-582.htm',
    'Telugu Desam': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1745.htm',
    'Janata Dal (United)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-805.htm',
    'Shiv Sena (Uddhav Balasaheb Thackrey)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-3369.htm',
    'Nationalist Congress Party – Sharadchandra Pawar': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-3620.htm',
    'Shiv Sena': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-3529.htm',
    'Lok Janshakti Party(Ram Vilas)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-3165.htm',
    'Yuvajana Sramika Rythu Congress Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1888.htm',
    'Rashtriya Janata Dal': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1420.htm',
    'Communist Party of India (Marxist)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-547.htm',
    'Indian Union Muslim League': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-772.htm',
    'Aam Aadmi Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1.htm',
    'Jharkhand Mukti Morcha': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-852.htm',
    'Janasena Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-860.htm',
    'Communist Party of India (Marxist-Leninist) (Liberation)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-545.htm',
    'Rashtriya Lok Dal': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1458.htm',
    'Jammu & Kashmir National Conference': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-834.htm',
    'United People’s Party, Liberal': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1998.htm',
    'Asom Gana Parishad': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-83.htm',
    'Hindustani Awam Morcha (Secular)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-664.htm',
    'Kerala Congress': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-911.htm',
    'Revolutionary Socialist Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1534.htm',
    'Nationalist Congress Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1142.htm',
    'Voice of the People Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-3388.htm',
    'Zoram People’s Movement': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-2757.htm',
    'Shiromani Akali Dal': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1584.htm',
    'Rashtriya Loktantrik Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-2484.htm',
    'Bharat Adivasi Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-3482.htm',
    'Sikkim Krantikari Morcha': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1658.htm',
    'Marumalarchi Dravida Munnetra Kazhagam': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-1046.htm',
    'Aazad Samaj Party (Kanshi Ram)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-2989.htm',
    'Apna Dal (Soneylal)': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-2070.htm',
    'AJSU Party': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-160.htm',
    'All India Majlis-E-Ittehadul Muslimeen': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-118.htm',
    'Independent': 'https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-743.htm'
}

# Function to scrape and save data for each party
def scrape_party_data(party_name, url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {party_name}. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table with the class 'table'
    table = soup.find('table', {'class': 'table'})
    if table is None:
        print(f'The detailed results table was not found for {party_name}.')
        return

    rows = table.find_all('tr')
    if not rows:
        print(f'No rows found in the table for {party_name}.')
        return

    # Extract table headers
    headers = [header.text.strip() for header in rows[0].find_all('th')]
    
    # Extract table data
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols:
            cols = [col.text.strip() for col in cols]
            data.append(cols)
    
    if not data:
        print(f'No data found for {party_name}.')
        return
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=headers)
    
    # Save to CSV
    csv_file = f'Party_Wise_Winning_Statistics/{party_name}.csv'
    df.to_csv(csv_file, index=False)
    print(f'Saved data for {party_name} to {csv_file}')

# Scrape data for each party
for party, url in party_urls.items():
    scrape_party_data(party, url)
