from bs4 import BeautifulSoup
import requests

def scrape_living():
    site = "https://www.buffalo.edu/campusliving.html"
    response = requests.get(site)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())
    section = soup.find_all('span', class_="teaser teaser-inline")
    print(section)
    section2 = soup.find_all('div', class_='teaser-title')
    print(section2)

def scrape_dining_halls():
    site = "https://ubdining.com/locations/whats-open"
    response = requests.get(site)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

def scrape_events():
    site = "https://www.buffalo.edu/studentlife/life-on-campus/clubs-and-activities.html"
    response = requests.get(site)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

def scrape_student_engagement():
    site = "https://www.buffalo.edu/studentlife/who-we-are/departments/engagement.html"
    response = requests.get(site)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

def scrape_frats_and_sororitoes():
    site = "https://www.buffalo.edu/studentlife/life-on-campus/clubs-and-activities/search/fraternity-and-sorority-life.html"
    response = requests.get(site)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

def scrape_true_blue():
    site = "https://www.buffalo.edu/trueblue.html"
    response = requests.get(site)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

def scrape_future_alumni_network():
    site = "https://www.buffalo.edu/alumni/get-involved/future-alumni-network.html"
    response = requests.get(site)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

if __name__ == '__main__':
    scrape_living()
