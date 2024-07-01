import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table", {"class": "table"})

data = []
for row in table.find_all("tr")[1:]:
    cols = row.find_all("td")
    if len(cols) >= 4:
        party = cols[0].text.strip()
        won = int(cols[1].text.strip())
        leading = int(cols[2].text.strip())
        total = int(cols[3].text.strip())
        data.append({"Party": party, "Won": won, "Leading": leading, "Total": total})

df = pd.DataFrame(data)
df.to_csv("election_results.csv", index=False)