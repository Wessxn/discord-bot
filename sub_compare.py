from bs4 import BeautifulSoup
import requests
import json

def get_subcount(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    json_str = scripts[36].text.split('var ytInitialData = ')[1].split(';')[0]
    data = json.loads(json_str)
    url_subcount = data["header"]["c4TabbedHeaderRenderer"]["subscriberCountText"]["simpleText"]
    return url_subcount
