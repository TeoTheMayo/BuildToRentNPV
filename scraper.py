import requests
from bs4 import BeautifulSoup
import json
import re

target_url = "https://www.redfin.com/LA/New-Orleans/2909-Hollygrove-St-70118/home/85499131"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

r = requests.get(target_url, headers=headers)

if r.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {r.status_code}")
    exit()

soup = BeautifulSoup(r.text, "html.parser")

scripts = soup.find_all('script')

script_found = None
for script in scripts:
    if script.string and "/* -- Data -- */" in script.string:
        script_found = script.string
        break

if script_found is None:
    print("Script containing '/* -- Data -- */' not found.")
    exit()

# Use regex to extract the JSON data
json_data_match = re.search(r'root\.__reactServerState\.InitialContext\s*=\s*({.*?});', script_found, re.DOTALL)

if not json_data_match:
    print("Failed to extract JSON data from the script.")
    exit()

json_data = json_data_match.group(1)


try:
    # Parse the JSON data
    data = json.loads(json_data)
    print("Parsed JSON Data:")
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")

if __name__ == '__main__':
    last_item = []
    for key, values in data.items():
        for ky, vl in values:
            last_item.append(ky)
print(last_item)