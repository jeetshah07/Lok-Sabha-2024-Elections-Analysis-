import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
os.makedirs('State_Wise_Results', exist_ok=True)

url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")

state_select = soup.find("select", {"id": "ctl00_ContentPlaceHolder1_Result1_ddlState"})
state_options = state_select.find_all("option")[1:]

all_state_results = []

for option in state_options:
    state_code = option["value"]
    state_name = option.text.strip()
    state_url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_code}.htm"
    state_response = requests.get(state_url)
    state_html = state_response.content
    state_soup = BeautifulSoup(state_html, "html.parser")
    
    state_table = state_soup.find("table", {"class": "table"})
    if state_table is not None:
        state_data = []
        for row in state_table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 4:
                party = cols[0].text.strip()
                won = int(cols[1].text.strip())
                leading = int(cols[2].text.strip())
                total = int(cols[3].text.strip())
                state_data.append({"Party": party, "Won": won, "Leading": leading, "Total": total})
        
        all_state_results.append({"State": state_name, "Data": state_data})
    else:
        print(f"The table element was not found for state: {state_name}")

for state in all_state_results:
    state_name = state["State"]
    state_data = state["Data"]
    state_df = pd.DataFrame(state_data)
    state_df.to_csv(f"State_Wise_Results/{state_name}_results.csv", index=False)
